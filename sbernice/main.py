from machine import Pin, SPI
from time import sleep_ms
import onewire
import ds18x20

# Zapnout po vyreseni zapojeni displeje podle popis.md.
POUZIT_MATICI = False

cidlo = ds18x20.DS18X20(onewire.OneWire(Pin(2)))
adresa = cidlo.scan()[0]


def zapis(registr, hodnota):
    cs.value(0)
    spi.write(bytes((registr, hodnota)))
    cs.value(1)


if POUZIT_MATICI:
    cs = Pin(17, Pin.OUT, value=1)
    spi = SPI(0, baudrate=500_000, polarity=0, phase=0,
              sck=Pin(18), mosi=Pin(19), miso=Pin(16))
    zapis(0x0C, 0)  # Displej vypnout pri nastavovani.
    zapis(0x0F, 0)  # Vypnout test.
    zapis(0x09, 0)  # Ovladat jednotlive LED.
    zapis(0x0B, 7)  # Pouzit vsech osm radku.
    zapis(0x0A, 1)  # Nizky jas.
    for radek in range(1, 9):
        zapis(radek, 0)
    zapis(0x0C, 1)  # Displej zapnout.

while True:
    cidlo.convert_temp()
    sleep_ms(750)
    teplota = cidlo.read_temp(adresa)
    print("Teplota:", teplota, "C")

    if POUZIT_MATICI:
        pocet = int(teplota / 5 + 0.5)  # Jeden radek = 5 stupnu.
        for radek in range(1, 9):
            zapis(radek, 255 if radek <= pocet else 0)
    sleep_ms(250)
