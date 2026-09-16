Chceme měřit teplotu a ukázat ji na displeji.
Pico čte čidlo DS18B20 přes 1-Wire a teplotu zobrazuje na displeji TM1637.
Displej ukazuje celé stupně a písmeno C, například 23C, a mění hodnotu přibližně jednou za sekundu.

```text
Pico WH                          DS18B20 (TO-92)
pin 36 (3V3 OUT / +) ──┬───────── 3 VDD (+)
                      │
                    4,7 kΩ
                      │
pin  4 (GP2) ─────────┴───────── 2 DQ (data)
pin  3 (GND / −) ─────────────── 1 GND (−)
```

Potřebujeme DS18B20, displej TM1637, rezistor 4,7 kΩ a vodiče.
Čísla pinů Pica jsou **fyzická**, označení GP patří do programu.
DS18B20 v pouzdře TO-92 má s plochou stranou k sobě a nožičkami dolů zleva GND, DQ, VDD.

```text
Pico WH                         Displej TM1637
pin 36 (3V3 OUT / +) ─────────── VCC
pin 38 (GND / −) ─────────────── GND
pin  6 (GP4) ────────────────── CLK
pin  7 (GP5) ────────────────── DIO
```

Čidlo i displej napájej z 3,3 V; pin 36 je společný pro oba.
Řiď se popisky na displeji, pořadí jeho čtyř pinů se může lišit.
Displej může ležet vedle breadboardu a nepotřebuje potenciometr ani další rezistor.
Zapoj bez USB, pak připoj USB a spusť `main.py`; další soubor s ovladačem není potřeba.
Dvojtečka zůstává zhasnutá; TM1637 používá vlastní přenos přes CLK a DIO, nikoli I²C.

Podklady: [piny Pico W/WH](https://datasheets.raspberrypi.com/picow/PicoW-A4-Pinout.pdf), [DS18B20](https://www.analog.com/media/en/technical-documentation/data-sheets/ds18b20.pdf), [TM1637](https://files.seeedstudio.com/wiki/Grove-4-Digit_Display/res/TM1637_datasheet.pdf), [příklad modulu pro 3,3 V](https://wiki.seeedstudio.com/Grove-4-Digit_Display/).
