Chceme tlačítkem přepínat dvě LED.
Po zapnutí svítí LED1, po stisku zhasne a rozsvítí se LED2.
Další stisk je přepne zpět; držení ani puštění tlačítka je nepřepíná.

```text
Pico WH
pin 19 (GP14) ── tlačítko ── pin 18 (GND / −)
pin 20 (GP15) ── 180 Ω ── 180 Ω ── LED1 (+)
pin 18 (GND / −) ───────────────── LED1 (−)
pin 17 (GP13) ── 180 Ω ── 180 Ω ── LED2 (+)
pin 18 (GND / −) ───────────────── LED2 (−)
```
