Chceme vytvořit elektronickou hrací kostku.
Po stisku tlačítka Pico přes SPI krátce střídá číslice na maticovém displeji 8×8 s MAX7219.
Potom zůstane svítit náhodná číslice od 1 do 6 až do dalšího stisku; po zapnutí se ukáže 1.

Zapojení při napájení Pica z USB:

```text
Pico WH                         Displej 8×8 s MAX7219
pin 40 (VBUS / +5 V z USB) ───── VCC (+)
pin 38 (GND / −) ─────────────── GND (−)
pin  5 (GP3 / SPI0 MOSI) ─────── DIN
pin  2 (GP1) ────────────────── CS
pin  4 (GP2 / SPI0 SCK) ──────── CLK

pin 19 (GP14) ── tlačítko ── pin 18 (GND / −)
```

Potřebujeme Pico WH, modul displeje s MAX7219, tlačítko a vodiče.
Použij vstupní konektor displeje označený DIN; druhý konektor nech volný.
Tlačítko nepotřebuje další rezistor, program zapíná vnitřní přitahovací rezistor Pica.
U čtyřnohého tlačítka použij dva vývody, které se propojí až stiskem.

Čísla pinů Pica v zapojení jsou **fyzická**, v programu `Pin(...)` používá číslo **GP**.
Při pohledu ze strany součástek s USB nahoře je pin 1 vlevo nahoře a pin 40 vpravo nahoře.
Zapoj bez USB, pak připoj USB a spusť `main.py`; další soubor s ovladačem není potřeba.
Orientaci číslic je potřeba ověřit na skutečném displeji; zapojení řádků a sloupců se může mezi moduly lišit.
