Chceme měnit jas dvou LED otáčením potenciometru.
V první polovině otáčení potenciometru roste jas LED1 od nuly do plného jasu a LED2 nesvítí.
Ve druhé polovině LED1 svítí naplno a jas LED2 roste od nuly do plného jasu.

```text
Pico WH                         Potenciometr
pin 36 (3V3 OUT / +) ─────────── krajní vývod
pin 31 (GP26) ───────────────── jezdec (obvykle prostřední)
pin 38 (GND / −) ─────────────── druhý krajní vývod

pin 20 (GP15) ── 180 Ω ── 180 Ω ── LED1 (+)
pin 18 (GND / −) ───────────────── LED1 (−)
pin 17 (GP13) ── 180 Ω ── 180 Ω ── LED2 (+)
pin 18 (GND / −) ───────────────── LED2 (−)
```
