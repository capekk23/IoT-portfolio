from machine import ADC, PWM, Pin
from time import sleep_ms

potenciometr = ADC(Pin(26))
led1 = PWM(Pin(15), freq=1000)
led2 = PWM(Pin(13), freq=1000)

while True:
    hodnota = potenciometr.read_u16()
    led1.duty_u16(min(hodnota * 2, 65535))
    led2.duty_u16(max(hodnota * 2 - 65535, 0))
    sleep_ms(10)
