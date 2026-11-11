"""Pico: I2C target at 0x42 for the Raspberry Pi.
Writing "T" toggles the LED and beeps, reading returns the LED state (0 or 1)."""
from machine import I2CTarget, Pin
import time

I2C_ADDRESS = 0x42
LED = Pin(14, Pin.OUT)     # LED through 2x 180 ohm to GP14
BUZZER = Pin(15, Pin.OUT)  # Active buzzer: + to GP15, - to GND

received = 0


# Runs right when the Pi writes or reads, so it must be short.
def on_i2c(target, buf=bytearray(1)):
    global received
    flags = target.irq().flags()
    if flags & I2CTarget.IRQ_WRITE_REQ:
        target.readinto(buf)
        received = buf[0]
    if flags & I2CTarget.IRQ_READ_REQ:
        buf[0] = LED.value()
        target.write(buf)


# GP0 (SDA) and GP1 (SCL) go to the Pi's SDA and SCL.
i2c = I2CTarget(0, I2C_ADDRESS, sda=Pin(0), scl=Pin(1))
i2c.irq(on_i2c, trigger=I2CTarget.IRQ_WRITE_REQ | I2CTarget.IRQ_READ_REQ, hard=True)

while True:
    if received == ord("T"):
        received = 0
        LED.toggle()
        BUZZER.on()
        time.sleep_ms(100)
        BUZZER.off()
        print("Toggle, LED:", LED.value())
    time.sleep_ms(5)
