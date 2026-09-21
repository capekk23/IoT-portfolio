from machine import Pin, SPI
from time import sleep_ms
from random import getrandbits

# Pin(...) pouziva cisla GP, ne fyzicka cisla pinu.
spi = SPI(0, baudrate=100_000, polarity=0, phase=0,
          sck=Pin(2), mosi=Pin(3))
cs = Pin(1, Pin.OUT, value=1)
tlacitko = Pin(14, Pin.IN, Pin.PULL_UP)

# Osm radku kazde cislice; jednicka znamena svitici bod.
cislice = (
    (0b00000000,
     0b00010000,
     0b00110000,
     0b00010000,
     0b00010000,
     0b00010000,
     0b00010000,
     0b00111000),
    (0b00000000,
     0b00111000,
     0b01000100,
     0b00000100,
     0b00001000,
     0b00010000,
     0b00100000,
     0b01111100),
    (0b00000000,
     0b00111000,
     0b01000100,
     0b00000100,
     0b00011000,
     0b00000100,
     0b01000100,
     0b00111000),
    (0b00000000,
     0b00001000,
     0b00011000,
     0b00101000,
     0b01001000,
     0b01111100,
     0b00001000,
     0b00001000),
    (0b00000000,
     0b01111100,
     0b01000000,
     0b01000000,
     0b01111000,
     0b00000100,
     0b01000100,
     0b00111000),
    (0b00000000,
     0b00111000,
     0b01000000,
     0b01000000,
     0b01111000,
     0b01000100,
     0b01000100,
     0b00111000),
)


def odesli(registr, hodnota):
    cs.off()
    spi.write(bytes((registr, hodnota)))
    cs.on()


def zobraz(cislo):
    for radek in range(8):
        odesli(radek + 1, cislice[cislo - 1][radek])


sleep_ms(50)
odesli(0x0F, 0)  # Vypnout test vsech LED.
odesli(0x0C, 0)  # Zhasnout behem nastaveni.
odesli(0x09, 0)  # Vlastni obrazce, bez dekodovani cislic.
odesli(0x0B, 7)  # Zobrazovat vsech osm radku.
odesli(0x0A, 1)  # Nizky jas.
zobraz(1)
odesli(0x0C, 1)  # Zapnout displej.

while True:
    if tlacitko.value() == 0:
        sleep_ms(20)  # Ustaleni kontaktu po stisku.
        if tlacitko.value() == 0:
            for krok in range(12):
                cislo = getrandbits(3)
                while cislo == 0 or cislo == 7:
                    cislo = getrandbits(3)
                zobraz(cislo)
                sleep_ms(50 + krok * 15)
            # Posledni cislo zustane svitit; drzeni nespusti dalsi hod.
            while tlacitko.value() == 0:
                sleep_ms(10)
            sleep_ms(20)
    sleep_ms(10)
