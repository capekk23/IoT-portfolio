Chceme měřit vzdálenost ultrazvukovým senzorem HC-SR04 a ukazovat ji na dvou displejích.
LCD 16×2 přes sběrnici I2C ukazuje vzdálenost v cm, matice 8×8 s MAX7219 přes sběrnici SPI ukazuje blízkost předmětu.
Každý centimetr navíc zhasne jednu LED matice: zhasínají ve spirále od okraje ke středu, do 6 cm svítí celá, od 70 cm je zhasnutá.

Náš HC-SR04 je novější verze s čipem RCWL-9610. Podle rezistorů na zadní straně umí režimy GPIO, I2C, UART a 1-Wire.
Plošky M1 a M2 jsou prázdné, takže senzor je v režimu GPIO (Trig/Echo), není na sběrnici.

```text
                           Raspberry Pi Pico WH (USB nahoře)
                         ┌─────────────────────────────────┐
Matice CS ──────── pin 2 ┤ GP1                             │
Matice CLK ─────── pin 4 ┤ GP2 (SPI0 SCK)                  │
Matice DIN ─────── pin 5 ┤ GP3 (SPI0 MOSI)                 │
LCD SDA ────────── pin 6 ┤ GP4 (I2C0 SDA)                  │
LCD SCL ────────── pin 7 ┤ GP5 (I2C0 SCL)                  │
HC-SR04 GND ───── pin 18 ┤ GND                             │
HC-SR04 Trig ──── pin 19 ┤ GP14                            │
HC-SR04 Echo* ─── pin 20 ┤ GP15                            │
                         │                      GND pin 38 ├──── lišta − ─┬─ LCD GND
                         │                                 │              └─ Matice GND
                         │        VBUS (+5 V z USB) pin 40 ├──── lišta + ─┬─ LCD VCC
                         │                                 │              ├─ Matice VCC
                         │                                 │              └─ HC-SR04 VCC
                         └─────────────────────────────────┘
* Echo přes dělič z rezistorů, viz níže.
```

Po vodičích:

```text
Pico WH                          LCD 16×2 s I2C převodníkem
lišta + (pin 40, VBUS 5 V) ────── VCC
lišta − (pin 38, GND) ─────────── GND
pin  6 (GP4 / I2C0 SDA) ──────── SDA
pin  7 (GP5 / I2C0 SCL) ──────── SCL

Pico WH                          Matice 8×8 s MAX7219 (konektor DIN)
lišta + (pin 40, VBUS 5 V) ────── VCC
lišta − (pin 38, GND) ─────────── GND
pin  5 (GP3 / SPI0 MOSI) ─────── DIN
pin  2 (GP1) ────────────────── CS
pin  4 (GP2 / SPI0 SCK) ──────── CLK

Pico WH                          HC-SR04
lišta + (pin 40, VBUS 5 V) ────── VCC
pin 18 (GND / −) ─────────────── GND
pin 19 (GP14) ───────────────── Trig
pin 20 (GP15) ──┬── 180 Ω ────── Echo
                └── 180 Ω ── 180 Ω ── GND
```

Pin 40 (+5 V) a pin 38 (GND) přiveď na napájecí lišty breadboardu, displeje i senzor ber z nich.
Senzor napájíme z 5 V, s 3,3 V nám nefungoval. Echo pak vrací 5 V, ale Pico snese jen 3,3 V, proto jsou na Echo tři rezistory 180 Ω jako dělič: do pinu jde asi 3,3 V.
Když LCD po spuštění nic neukazuje, otoč šroubkem modrého trimru na převodníku (kontrast).
Ze kterého rohu spirála začíná, záleží na natočení modulu; ověř na skutečném displeji.
Čísla pinů Pica v zapojení jsou **fyzická**, v programu `Pin(...)` používá číslo **GP**.
Při pohledu ze strany součástek s USB nahoře je pin 1 vlevo nahoře a pin 40 vpravo nahoře.
