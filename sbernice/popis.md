Chceme měřit teplotu a ukázat ji na displeji.
Pico čte čidlo DS18B20 přes 1-Wire a pro displej MAX7219 je připravený přenos přes SPI.
Displej je zatím v programu vypnutý, protože musíme ověřit, zda zvládne řízení z Pica při napětí 3,3 V.

```text
Pico WH                          DS18B20 (TO-92)
pin 36 (3V3 OUT / +) ──┬───────── 3 VDD (+)
                      │
                    4,7 kΩ
                      │
pin  4 (GP2) ─────────┴───────── 2 DQ (data)
pin  3 (GND / −) ─────────────── 1 GND (−)
```

Čísla vlevo jsou fyzické piny Pica, GP je označení v programu.
U samotného DS18B20 v pouzdře TO-92, s plochou stranou k sobě a nožičkami dolů, jsou vývody zleva 1, 2, 3.
U čidla na destičce nebo na kabelu se řiďte jeho popisky, ne tímto pořadím.
Zapojovat bez napájení; Pico potom napájet přes USB.

**Displej — zatím nezapojovat, nejdřív vyřešit převod signálů z 3,3 V na 5 V.**

```text
Pico WH                         Převod signálů       Modul MAX7219
pin 25 (GP19) ───────────────── 3,3 V → 5 V ─────── DIN
pin 24 (GP18) ───────────────── 3,3 V → 5 V ─────── CLK
pin 22 (GP17) ───────────────── 3,3 V → 5 V ─────── CS / LOAD
pin 23 (GND / −) ────────────── společná zem ────── GND (−)
pin 40 (VBUS / +5 V z USB) ─────────────────────── VCC (+)

DOUT displeje: nezapojovat
```

MAX7219 při 5V napájení vyžaduje pro signál „1“ alespoň 3,5 V; Pico dává 3,3 V.
Převodník v seznamu dílů není a nevíme, zda ho obsahuje váš modul.
Nákres displeje je proto jen návrh; převodník potřebuje také vlastní napájení podle svého typu.
Napájení z USB musí zvládnout odběr Pica i displeje a na GP piny nesmí přijít 5 V.
Po vyřešení zapojení zapněte v programu `POUZIT_MATICI = True`.

Ověřeno podle [pinů Pica W/WH](https://datasheets.raspberrypi.com/picow/PicoW-A4-Pinout.pdf), [DS18B20, strany 2, 4 a 7](https://www.analog.com/media/en/technical-documentation/data-sheets/ds18b20.pdf) a [MAX7219, strany 2, 3 a 5](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX7219-MAX7221.pdf).
