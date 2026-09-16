from machine import Pin
from time import sleep_ms

led1 = Pin(15, Pin.OUT, value=1)
led2 = Pin(13, Pin.OUT, value=0)
tlacitko = Pin(14, Pin.IN, Pin.PULL_UP)

while True:
    if tlacitko.value() == 0:
        led1.toggle()
        led2.toggle()
        sleep_ms(50)
        while tlacitko.value() == 0:
            sleep_ms(10)
        sleep_ms(50)
    sleep_ms(10)
