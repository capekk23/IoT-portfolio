from machine import Pin, UART
from neopixel import NeoPixel
from time import ticks_ms, ticks_diff, sleep_ms
import network
import socket
import select

# Pico 2: modry hrac, odesilani stisku a prijem barev pres Wi-Fi.
# Pin(...) pouziva cislo GP, nikoli fyzicke cislo pinu.
tlacitko = Pin(14, Pin.IN, Pin.PULL_UP)
kruh = NeoPixel(Pin(15), 8)
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
kruh.fill((0, 0, 0))
kruh.write()

wifi = network.WLAN(network.WLAN.IF_STA)
wifi.active(True)
wifi.connect("Pico-pretahovana")
while not wifi.isconnected():
    sleep_ms(100)

spojeni = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
spojeni.bind(("0.0.0.0", 5000))
cekani = select.poll()
cekani.register(spojeni, select.POLLIN)
pico1 = ("192.168.4.1", 5000)

posledni_stav = tlacitko.value()
ustaleny_stav = posledni_stav
cas_zmeny = ticks_ms()
cas_zadosti = ticks_ms()
hra_bezi = False

while True:
    ted = ticks_ms()

    # Jeden bajt B znamena jeden stisk. Drzeni dalsi bajty neposila.
    stav = tlacitko.value()
    if stav != posledni_stav:
        posledni_stav = stav
        cas_zmeny = ted
    if stav != ustaleny_stav and ticks_diff(ted, cas_zmeny) >= 20:
        ustaleny_stav = stav
        if stav == 0 and hra_bezi:
            uart.write(b"B")

    # Pravidelna zadost obnovi obraz i po ztrate jednoho UDP paketu.
    if ticks_diff(ted, cas_zadosti) >= 50:
        cas_zadosti = ted
        spojeni.sendto(b"?", pico1)

    if cekani.poll(0):
        barvy, adresa = spojeni.recvfrom(32)
        if adresa == pico1 and len(barvy) == 24:
            for pixel in range(8):
                zacatek = pixel * 3
                kruh[pixel] = (barvy[zacatek], barvy[zacatek + 1], barvy[zacatek + 2])
            kruh.write()
            hra_bezi = True

    sleep_ms(2)
