Chceme tlačítkem měnit rychlost střídání dvou LED na Raspberry Pi 4.
Po spuštění svítí LED1 a LED2 je zhasnutá; každých 100 ms se prohodí.
Každý stisk přepne interval na další hodnotu: 100, 250, 500, 1000, 1500 a 2000 ms, potom znovu 100 ms; držení ani puštění tlačítka rychlost nemění.

```text
Raspberry Pi 4
pin  8 (GPIO14) ── tlačítko ── GND / −
pin 10 (GPIO15) ── 180 Ω ── LED1 (+)
GND / − ────────────────── LED1 (−)
pin 36 (GPIO16) ── 180 Ω ── LED2 (+)
GND / − ────────────────── LED2 (−)
```

Všechny země jsou společné, na Pi lze použít například pin 6 (GND / −).
Čísla pinů v zapojení jsou **fyzická**, program používá čísla **BCM GPIO** v závorkách.
Tlačítko používá vnitřní pull-up; program přijme změnu až po 30 ms stabilního stavu, aby jeden stisk nezapočítal vícekrát.
Interval je čas do prohození LED, takže při 100 ms každá LED 100 ms svítí a 100 ms nesvítí.
Piny jsou ověřené podle výpisu `pinout` na naší desce a [dokumentace Raspberry Pi](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#gpio-and-the-40-pin-header).

Program [main.rs](main.rs) je napsaný v Rustu a GPIO ovládá knihovnou `rppal`.
Na Raspberry Pi potřebujeme Rust a Cargo (`sudo apt install rustc cargo`).
Ve složce úlohy ho přeložíme a spustíme:

```sh
cargo run --release --locked
```

Spouštěj jen jednu instanci programu. Pokud ještě běží naše služba z ladění, nejdřív ji zastav příkazem `systemctl --user stop rpi-digi`.
Program ukončíš pomocí Ctrl+C.

[Video zapojení](fotky/IMG_3382.MOV)
