# Raspberry Pi: I2C controller. The Pi has no analog input, so it reads the
# potentiometer from the Pico and sends back the LED brightness.
# The button (or the dashboard) toggles the LED on the Pico.
require "socket"

PICO = 0x42          # I2C address of the Pico
I2C_SLAVE = 0x0703   # Linux ioctl that selects the target address
BUTTON = 17          # BCM GPIO number, physical pin 11

i2c = File.open("/dev/i2c-1", "r+b")
i2c.ioctl(I2C_SLAVE, PICO)
bus = Mutex.new      # The button, the web and the main loop share one bus.

led = 1
pot = 0
brightness = 0
override = nil       # Brightness from the dashboard slider
override_pot = 0     # Potentiometer position when the slider was moved
presses = 0

toggle = lambda do
  bus.synchronize { i2c.syswrite("T") }
  presses += 1
end

# gpiomon prints one line for every press (falling edge, pull-up, 30 ms debounce).
Thread.new do
  IO.popen(["gpiomon", "-c", "gpiochip0", "-b", "pull-up", "-e", "falling", "-p", "30ms", BUTTON.to_s]) do |events|
    events.each_line { toggle.call }
  end
end

# GET /stav returns the state as JSON, POST /tlacitko is the logical button,
# POST /jas/50 sets the brightness until the real potentiometer moves.
Thread.new do
  server = TCPServer.new("0.0.0.0", 8009)
  loop do
    client = server.accept
    request = client.gets.to_s
    while (line = client.gets) && line != "\r\n"
    end

    toggle.call if request.start_with?("POST /tlacitko")
    if request.start_with?("POST /jas/")
      override = request[10..].to_i.clamp(0, 100)
      override_pot = pot
    end

    json = "{\"led\":#{led},\"pot\":#{pot},\"jas\":#{brightness}," \
           "\"logicky\":#{!override.nil?},\"stisky\":#{presses}}"
    client.write "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n" \
                 "Access-Control-Allow-Origin: *\r\nContent-Length: #{json.size}\r\n" \
                 "Connection: close\r\n\r\n#{json}"
    client.close
  end
end

loop do
  # Read 3 bytes from the Pico: LED on, potentiometer %, brightness %.
  led, pot, brightness = bus.synchronize { i2c.sysread(3).bytes }

  # Moving the real potentiometer takes control back from the dashboard.
  override = nil if override && (pot - override_pot).abs > 3
  wanted = override || pot

  bus.synchronize { i2c.syswrite("J" + wanted.chr) } if wanted != brightness
  sleep 0.05
end
