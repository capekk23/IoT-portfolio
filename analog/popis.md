Chceme měnit jas LED otáčením potenciometru.
Pico měří napětí z potenciometru a podle něj nastaví jas LED.
Otáčením tak LED zeslabujeme nebo zesilujeme.

```text
Pico WH                         Potenciometr
pin 36 (3V3 OUT / +) ─────────── krajní vývod
pin 31 (GP26) ───────────────── jezdec (obvykle prostřední)
pin 38 (GND / −) ─────────────── druhý krajní vývod

pin 20 (GP15) ── 180 Ω ── 180 Ω ── LED (+)
pin 18 (GND / −) ───────────────── LED (−)
```

Čísla jsou fyzické piny Pica, GP je označení v programu.
Zapojovat bez napájení; Pico potom napájet přes USB.
Potenciometr připojte na 3,3 V, ne na 5 V.
U běžné LED je delší nožička + a kratší − (u ploché strany).
Přesný typ potenciometru a LED neznáme, polohu jejich vývodů je potřeba ověřit na vašich dílech.

Piny ověřeny: [Pico W/WH](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html), [nákres pinů](https://datasheets.raspberrypi.com/picow/PicoW-A4-Pinout.pdf).
