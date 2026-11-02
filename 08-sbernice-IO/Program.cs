using System.Device.Gpio;
using System.Device.I2c;
using System.Device.Spi;
using System.Diagnostics;
using System.Globalization;
using System.Net;
using System.Text;

// Decimal point instead of comma, so the JSON for the dashboard stays valid.
CultureInfo.DefaultThreadCurrentCulture = CultureInfo.InvariantCulture;
CultureInfo.CurrentCulture = CultureInfo.InvariantCulture;

// GPIO numbers are BCM, not the physical header pin numbers.
var gpio = new GpioController();
var trig = gpio.OpenPin(23, PinMode.Output, PinValue.Low);
var echo = gpio.OpenPin(24, PinMode.Input);

// LCD on I2C bus 1 (pins 3 and 5), our module is at 0x27 (others use 0x3F).
var lcd = I2cDevice.Create(new I2cConnectionSettings(1, 0x27));
// Matrix on SPI0, chip select CE0 (pin 24).
var spi = SpiDevice.Create(new SpiConnectionSettings(0, 0) { ClockFrequency = 100_000, Mode = SpiMode.Mode0 });

// State shared with the web thread for the dashboard.
double cm = -1;
int lit = 0;
string[] lcdLines = { "", "" };
double fakeCm = -1;
var fakeUntil = DateTime.MinValue;

// LCD through the PCF8574 expander:
// bits 4-7 = data, bit 3 = backlight, bit 2 = E, bit 0 = RS.
void Pulse(int data)
{
    data |= 0x08;
    lcd.Write(new byte[] { (byte)data, (byte)(data | 0x04), (byte)data });
}

void Send(int value, int rs = 0)
{
    Pulse((value & 0xF0) | rs);
    Pulse(((value << 4) & 0xF0) | rs);
}

void Print(int row, string text)
{
    lcdLines[row] = text;
    Send(0x80 + row * 0x40);  // Start of row 0 or 1.
    foreach (char c in text.PadRight(16))
    {
        Send(c, 1);
    }
}

// 8x8 matrix with MAX7219: register and value.
void Matrix(int register, int value)
{
    spi.Write(new byte[] { (byte)register, (byte)value });
}

// LED order in a spiral: from the edge clockwise to the centre.
var spiral = new List<(int Row, int Col)>();
int top = 0, bottom = 7, left = 0, right = 7;
while (top < bottom)
{
    for (int c = left; c <= right; c++) spiral.Add((top, c));
    for (int r = top + 1; r <= bottom; r++) spiral.Add((r, right));
    for (int c = right - 1; c >= left; c--) spiral.Add((bottom, c));
    for (int r = bottom - 1; r > top; r--) spiral.Add((r, left));
    top++;
    bottom--;
    left++;
    right--;
}

// Light the last "count" LEDs of the spiral; the edge goes dark first.
void Draw(int count)
{
    var rows = new int[8];
    foreach (var (r, c) in spiral.Skip(64 - count))
    {
        rows[r] |= 0x80 >> c;
    }
    for (int r = 0; r < 8; r++)
    {
        Matrix(r + 1, rows[r]);
    }
}

// Waits for the echo pin to reach the value, at most 30 ms.
bool WaitFor(PinValue value, Stopwatch timer)
{
    while (echo.Read() != value)
    {
        if (timer.ElapsedMilliseconds > 30) return false;
    }
    return true;
}

// Distance in cm, or -1 when nothing is in range.
double Measure()
{
    // With no echo the sensor keeps Echo high for ~200 ms; wait until it is ready again.
    var ready = Stopwatch.StartNew();
    while (echo.Read() == PinValue.High && ready.ElapsedMilliseconds < 300) { }

    // A 10 us pulse on Trig starts the measurement.
    var timer = Stopwatch.StartNew();
    trig.Write(PinValue.High);
    while (timer.Elapsed.TotalMicroseconds < 10) { }
    trig.Write(PinValue.Low);

    if (!WaitFor(PinValue.High, timer)) return -1;
    var start = timer.Elapsed.TotalMicroseconds;
    if (!WaitFor(PinValue.Low, timer)) return -1;
    // 58 us of echo is 1 cm there and back.
    return (timer.Elapsed.TotalMicroseconds - start) / 58;
}

// GET /stav returns the state as JSON, POST /vzdalenost/30 fakes 30 cm for 3 s.
new Thread(() =>
{
    var web = new HttpListener();
    web.Prefixes.Add("http://*:8008/");
    web.Start();
    while (true)
    {
        var ctx = web.GetContext();
        var path = ctx.Request.Url.AbsolutePath;
        if (ctx.Request.HttpMethod == "POST" && path.StartsWith("/vzdalenost/"))
        {
            fakeCm = double.Parse(path.Substring(12));
            fakeUntil = DateTime.Now.AddSeconds(3);
        }
        var json = $"{{\"cm\":{cm:0.0},\"led\":{lit},\"lcd\":[\"{lcdLines[0]}\",\"{lcdLines[1]}\"],\"logicka\":{(DateTime.Now < fakeUntil ? "true" : "false")}}}";
        var body = Encoding.UTF8.GetBytes(json);
        ctx.Response.ContentType = "application/json";
        ctx.Response.AddHeader("Access-Control-Allow-Origin", "*");
        ctx.Response.OutputStream.Write(body);
        ctx.Response.Close();
    }
}).Start();

// Switch the LCD to 4-bit mode.
Thread.Sleep(50);
for (int i = 0; i < 3; i++)
{
    Pulse(0x30);
    Thread.Sleep(5);
}
Pulse(0x20);
Send(0x28);  // 4 bits, 2 rows.
Send(0x0C);  // Display on, no cursor.
Send(0x06);  // Cursor moves right.
Send(0x01);  // Clear the display.
Thread.Sleep(2);

Matrix(0x0F, 0);  // Display test off.
Matrix(0x0C, 0);  // Dark while setting up.
Matrix(0x09, 0);  // Own patterns, no digit decoding.
Matrix(0x0B, 7);  // Show all eight rows.
Matrix(0x0A, 1);  // Low brightness.
for (int r = 1; r <= 8; r++)
{
    Matrix(r, 0);
}
Matrix(0x0C, 1);  // Matrix on.

Print(0, "Vzdalenost:");

while (true)
{
    // The dashboard slider replaces the sensor for 3 s after the last move.
    cm = DateTime.Now < fakeUntil ? fakeCm : Measure();
    int target;
    if (cm < 0)
    {
        Print(1, "mimo rozsah");
        target = 0;
    }
    else
    {
        Print(1, $"{cm:0.0} cm");
        // Each cm = one LED: all 64 lit up to 6 cm, none from 70 cm.
        target = Math.Clamp(70 - (int)cm, 0, 64);
    }
    // Animation: one LED at a time towards the new state.
    while (lit != target)
    {
        lit += lit < target ? 1 : -1;
        Draw(lit);
        Thread.Sleep(10);
    }
    Thread.Sleep(100);
}
