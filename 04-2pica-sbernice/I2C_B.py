"""Pico B: I2C target at 0x42, toggles the LED and beeps when it receives "T"."""
from machine import I2CTarget, Pin
import time

I2C_ADDRESS = 0x42
LED = Pin(14, Pin.OUT)     # LED through 2x 180 ohm to GP14
BUZZER = Pin(15, Pin.OUT)  # Active buzzer: + to GP15, - to GND

received = 0


# Runs right when Pico A writes a byte, so it only stores it for the main loop.
def on_write(target, buf=bytearray(1)):
    global received
    if target.irq().flags() & I2CTarget.IRQ_WRITE_REQ:
        target.readinto(buf)
        received = buf[0]


# Wire GP0 (SDA) and GP1 (SCL) to the other Pico's matching pins.
i2c = I2CTarget(0, I2C_ADDRESS, sda=Pin(0), scl=Pin(1))
i2c.irq(on_write, trigger=I2CTarget.IRQ_WRITE_REQ, hard=True)

while True:
    if received == ord("T"):
        received = 0
        LED.toggle()
        BUZZER.on()
        time.sleep_ms(100)
        BUZZER.off()
        print("Toggle received")
    time.sleep_ms(5)
