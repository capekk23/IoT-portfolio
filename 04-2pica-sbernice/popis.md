Dvě Pica spolu mluví po sběrnici I2C.
Pico A (controller) po stisku tlačítka pošle na adresu 0x42 písmeno „T“.
Pico B (target) ho přijme, přepne LED a krátce pípne bzučákem.

Pico A má program [I2C.py](I2C.py), Pico B program [I2C_B.py](I2C_B.py).
Pico B používá `machine.I2CTarget`, které je v MicroPythonu od verze 1.25. Na Picu B proto musí být MicroPython 1.25 nebo novější.
Pull-upy na SDA a SCL zapíná I2C na Picu A.

```text
Pico A                           Pico B
pin 1 (GP0 / I2C0 SDA) ───────── pin 1 (GP0 / I2C0 SDA)
pin 2 (GP1 / I2C0 SCL) ───────── pin 2 (GP1 / I2C0 SCL)
pin 3 (GND / −) ──────────────── pin 3 (GND / −)

Pico A
pin 19 (GP14) ── tlačítko ── pin 18 (GND / −)

Pico B
pin 19 (GP14) ── 180 Ω ── 180 Ω ── LED (+)
pin 18 (GND / −) ───────────────── LED (−)
pin 20 (GP15) ──────────────────── bzučák (+)   (aktivní bzučák)
pin 23 (GND / −) ───────────────── bzučák (−)
```

U I2C se vodiče nekříží: SDA vede na SDA a SCL na SCL. Země obou Pic musí být propojené.
Každé Pico napájej vlastním USB, piny 36 ani 40 mezi Picy nepropojuj.
Čísla pinů Pica v zapojení jsou **fyzická**, v programu `Pin(...)` používá číslo **GP**.
