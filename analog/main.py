from machine import ADC, PWM, Pin
from time import sleep_ms

potenciometr = ADC(Pin(26))
led = PWM(Pin(15), freq=1000)

while True:
    led.duty_u16(potenciometr.read_u16())
    sleep_ms(10)
