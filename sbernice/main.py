from machine import Pin, I2C, SPI, time_pulse_us
from time import sleep_ms, sleep_us

# Pin(...) pouziva cisla GP, ne fyzicka cisla pinu.
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100_000)
spi = SPI(0, baudrate=100_000, polarity=0, phase=0,
          sck=Pin(2), mosi=Pin(3))
cs = Pin(1, Pin.OUT, value=1)
trig = Pin(14, Pin.OUT, value=0)
echo = Pin(15, Pin.IN)

# Adresa naseho LCD na I2C (jine kusy mivaji 0x3F).
adresa = 0x27


# LCD pres prevodnik PCF8574:
# bity 4-7 = data, bit 3 = podsviceni, bit 2 = E, bit 0 = RS.
def pul(data):
    data = data | 0x08
    try:
        i2c.writeto(adresa, bytes((data, data | 0x04, data)))
    except OSError:
        pass  # LCD neodpovida; program bezi dal bez nej.


def posli(bajt, rs=0):
    pul((bajt & 0xF0) | rs)
    pul(((bajt << 4) & 0xF0) | rs)


def napis(radek, text):
    posli(0x80 + radek * 0x40)  # Zacatek radku 0 nebo 1.
    for znak in "{:<16}".format(text):
        posli(ord(znak), 1)


# Matice 8x8 s MAX7219: registr a hodnota.
def matice(registr, hodnota):
    cs.off()
    spi.write(bytes((registr, hodnota)))
    cs.on()


# Poradi LED ve spirale: od okraje po smeru hodinovych rucicek ke stredu.
spirala = []
horni, dolni, levy, pravy = 0, 7, 0, 7
while horni < dolni:
    for sloupec in range(levy, pravy + 1):
        spirala.append((horni, sloupec))
    for radek in range(horni + 1, dolni + 1):
        spirala.append((radek, pravy))
    for sloupec in range(pravy - 1, levy - 1, -1):
        spirala.append((dolni, sloupec))
    for radek in range(dolni - 1, horni, -1):
        spirala.append((radek, levy))
    horni += 1
    dolni -= 1
    levy += 1
    pravy -= 1


# Rozsviti poslednich "pocet" LED spiraly; okraj zhasina jako prvni.
def kresli(pocet):
    radky = [0] * 8
    for radek, sloupec in spirala[64 - pocet:]:
        radky[radek] |= 0x80 >> sloupec
    for radek in range(8):
        matice(radek + 1, radky[radek])


# Prepnuti LCD do 4bitoveho rezimu.
sleep_ms(50)
for i in range(3):
    pul(0x30)
    sleep_ms(5)
pul(0x20)
posli(0x28)  # 4 bity, 2 radky.
posli(0x0C)  # Displej zapnout, bez kurzoru.
posli(0x06)  # Kurzor se posouva doprava.
posli(0x01)  # Smazat displej.
sleep_ms(2)

matice(0x0F, 0)  # Vypnout test vsech LED.
matice(0x0C, 0)  # Zhasnout behem nastaveni.
matice(0x09, 0)  # Vlastni obrazce, bez dekodovani cislic.
matice(0x0B, 7)  # Zobrazovat vsech osm radku.
matice(0x0A, 1)  # Nizky jas.
for radek in range(1, 9):
    matice(radek, 0)
matice(0x0C, 1)  # Zapnout matici.

napis(0, "Vzdalenost:")
svitici = 0

while True:
    # Puls 10 us na Trig spusti mereni.
    trig.on()
    sleep_us(10)
    trig.off()
    # Delka pulsu na Echo v us; 58 us odpovida 1 cm tam a zpet.
    cas = time_pulse_us(echo, 1, 30000)
    if cas < 0:
        napis(1, "mimo rozsah")
        cil = 0
    else:
        cm = cas / 58
        napis(1, "{:.1f} cm".format(cm))
        # Kazdy cm = jedna LED: do 6 cm sviti vsech 64, od 70 cm nic.
        cil = max(0, min(64, 70 - int(cm)))
    # Animace: k novemu stavu po jedne LED.
    while svitici != cil:
        if svitici < cil:
            svitici += 1
        else:
            svitici -= 1
        kresli(svitici)
        sleep_ms(10)
    sleep_ms(100)
