"""Pico as an "I2C ADC" for the Raspberry Pi (target at 0x42).
The Pi has no analog input, so it reads the potentiometer from the Pico
and sends back the LED brightness.

Protocol:
  write "T"            toggle the LED on/off (and beep)
  write "J", 0..100    set the LED brightness in %
  read 3 bytes         LED on (0/1), potentiometer %, brightness %
"""
from machine import ADC, I2CTarget, PWM, Pin
import time

I2C_ADDRESS = 0x42
led = PWM(Pin(14), freq=1000)  # LED through 2x 180 ohm to GP14
buzzer = Pin(15, Pin.OUT)      # Active buzzer: + to GP15, - to GND
pot = ADC(26)                  # Potentiometer wiper on GP26

state = bytearray(3)  # What the Pi reads: LED on, potentiometer %, brightness %
state[0] = 1
command = 0
toggle = False
index = 0


# Runs right when the Pi writes or reads a byte, so it must be short.
def on_i2c(target, buf=bytearray(1)):
    global command, toggle, index
    flags = target.irq().flags()
    if flags & I2CTarget.IRQ_WRITE_REQ:
        target.readinto(buf)
        if command == ord("J"):
            state[2] = min(buf[0], 100)
            command = 0
        elif buf[0] == ord("T"):
            toggle = True
        else:
            command = buf[0]
    if flags & I2CTarget.IRQ_READ_REQ:
        buf[0] = state[index] if index < 3 else 0
        index += 1
        target.write(buf)
    if flags & I2CTarget.IRQ_END_READ:
        index = 0
    if flags & I2CTarget.IRQ_END_WRITE:
        command = 0


# GP0 (SDA) and GP1 (SCL) go to the Pi's SDA and SCL.
i2c = I2CTarget(0, I2C_ADDRESS, sda=Pin(0), scl=Pin(1))
i2c.irq(on_i2c, hard=True, trigger=I2CTarget.IRQ_WRITE_REQ | I2CTarget.IRQ_READ_REQ
        | I2CTarget.IRQ_END_READ | I2CTarget.IRQ_END_WRITE)

while True:
    state[1] = pot.read_u16() * 100 // 65535

    if toggle:
        toggle = False
        state[0] ^= 1
        buzzer.on()
        time.sleep_ms(100)
        buzzer.off()

    led.duty_u16(state[2] * 65535 // 100 if state[0] else 0)
    time.sleep_ms(20)
