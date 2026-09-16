from machine import Pin
from time import sleep_ms, sleep_us
import onewire
import ds18x20

clk = Pin(4, Pin.OUT, value=1)
dio = Pin(5, Pin.OPEN_DRAIN, Pin.PULL_UP, value=1)
cidlo = ds18x20.DS18X20(onewire.OneWire(Pin(2)))
adresa = cidlo.scan()[0]
segmenty = dict(zip("0123456789 -C",
                   (0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D,
                    0x07, 0x7F, 0x6F, 0x00, 0x40, 0x39)))


def odesli(bajty):
    dio.off()  # Zacatek prenosu.
    sleep_us(10)
    for bajt in bajty:
        for bit in range(8):
            clk.off()
            dio.value((bajt >> bit) & 1)
            sleep_us(10)
            clk.on()
            sleep_us(10)
        clk.off()
        dio.on()  # Uvolnit DIO pro odpoved displeje.
        sleep_us(10)
        clk.on()
        sleep_us(10)
        clk.off()
        sleep_us(10)
    dio.off()
    sleep_us(10)
    clk.on()
    sleep_us(10)
    dio.on()  # Konec prenosu.
    sleep_us(10)


sleep_ms(50)
odesli([0x40])  # Zapis postupne do vsech ctyr mist.
odesli([0xC0, 0, 0, 0, 0])
odesli([0x89])  # Zapnout displej, nizky jas.

while True:
    cidlo.convert_temp()
    sleep_ms(750)
    teplota = round(cidlo.read_temp(adresa))
    text = "%3dC" % teplota
    odesli([0xC0] + [segmenty[znak] for znak in text])
    sleep_ms(250)
