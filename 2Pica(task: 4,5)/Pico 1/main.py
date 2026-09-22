from machine import Pin, UART
from neopixel import NeoPixel
from time import ticks_ms, ticks_diff, sleep_ms
import network
import socket
import select

# Pico 1: cerveny hrac, vypocet hry a Wi-Fi pristupovy bod.
# Pin(...) pouziva cislo GP, nikoli fyzicke cislo pinu.
tlacitko = Pin(14, Pin.IN, Pin.PULL_UP)
kruh = NeoPixel(Pin(15), 8)
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
JAS = 24  # Maximum je 255; kvuli napajeni z 3V3 ponechame nizky jas.
NASKOK = 20

kruh.fill((0, 0, 0))
kruh.write()

# Vlastni otevrena sit pro hru, bez routeru a bez internetu.
wifi = network.WLAN(network.WLAN.IF_AP)
wifi.config(ssid="Pico-pretahovana", security=0)
wifi.active(True)
wifi.ifconfig(("192.168.4.1", "255.255.255.0", "192.168.4.1", "192.168.4.1"))

spojeni = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
spojeni.bind(("0.0.0.0", 5000))
cekani = select.poll()
cekani.register(spojeni, select.POLLIN)


def barvy_kruhu(stisky1, stisky2, vitez):
    barvy = bytearray()
    skore = stisky1 - stisky2
    for pixel in range(8):
        # Vzdalenost od cerveneho bodu 0; modry bod je naproti na 4.
        vzdalenost = min(pixel, 8 - pixel)
        if vitez == 1:
            cervena, modra = JAS, 0
        elif vitez == 2:
            cervena, modra = 0, JAS
        elif stisky1 + stisky2 < 20:
            # Pet stisku rozsiri barvu o jeden pixel na kazdou stranu.
            podil1 = max(0, min(1, 1 + stisky1 / 5 - vzdalenost))
            podil2 = max(0, min(1, 1 + stisky2 / 5 - (4 - vzdalenost)))
            soucet = max(1, podil1 + podil2)
            cervena = int(JAS * podil1 / soucet)
            modra = int(JAS * podil2 / soucet)
        else:
            # Po setkani barev posouvame obe hranice podle naskoku.
            hranice = 2 + 2 * skore / NASKOK
            podil1 = max(0, min(1, hranice - vzdalenost + 0.5))
            cervena = int(JAS * podil1)
            modra = JAS - cervena
        barvy.extend((cervena, 0, modra))
    return barvy


def zobraz(barvy):
    for pixel in range(8):
        zacatek = pixel * 3
        kruh[pixel] = (barvy[zacatek], barvy[zacatek + 1], barvy[zacatek + 2])
    kruh.write()


# Zacneme az po prvni zadosti o obraz z Pica 2.
while True:
    zprava, adresa = spojeni.recvfrom(32)
    if zprava == b"?":
        break
uart.read()  # Zahodit pripadne stisky pred zacatkem hry.

stisky1 = 0
stisky2 = 0
vitez = 0
cas_vyhry = ticks_ms()
barvy = barvy_kruhu(stisky1, stisky2, vitez)
zobraz(barvy)
spojeni.sendto(barvy, adresa)

posledni_stav = tlacitko.value()
ustaleny_stav = posledni_stav
cas_zmeny = ticks_ms()
cas_obrazku = ticks_ms()

while True:
    ted = ticks_ms()

    # Kontakty musi zustat 20 ms ve stejnem stavu. Smycka pritom bezi dal.
    stav = tlacitko.value()
    if stav != posledni_stav:
        posledni_stav = stav
        cas_zmeny = ted
    if stav != ustaleny_stav and ticks_diff(ted, cas_zmeny) >= 20:
        ustaleny_stav = stav
        if stav == 0 and vitez == 0:
            stisky1 += 1

    if uart.any():
        zprava = uart.read()
        if vitez == 0:
            stisky2 += zprava.count(b"B")

    if vitez != 0 and ticks_diff(ted, cas_vyhry) >= 3000:
        stisky1 = 0
        stisky2 = 0
        vitez = 0

    if ticks_diff(ted, cas_obrazku) >= 50:
        cas_obrazku = ted
        skore = stisky1 - stisky2
        if vitez == 0 and abs(skore) >= NASKOK:
            vitez = 1 if skore > 0 else 2
            cas_vyhry = ted
        barvy = barvy_kruhu(stisky1, stisky2, vitez)
        zobraz(barvy)

    # Wi-Fi prenasi jen zadost a 24 bajtu RGB, zadne stisky.
    if cekani.poll(0):
        zprava, adresa = spojeni.recvfrom(32)
        if zprava == b"?":
            spojeni.sendto(barvy, adresa)

    sleep_ms(2)
