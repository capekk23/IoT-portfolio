Chceme měnit jas dvou LED otáčením potenciometru na Raspberry Pi 4.
Pi nemá analogový vstup, proto jde o „fake analog input“: měříme, jak dlouho se kondenzátor nabíjí přes potenciometr. Čím větší odpor, tím delší čas.
V první polovině otáčení roste jas LED1 a LED2 nesvítí, ve druhé polovině svítí LED1 naplno a roste jas LED2.

| Odkud | Kam |
|---|---|
| pin 1 (3V3, +) | krajní vývod potenciometru B10K |
| jezdec potenciometru (prostřední vývod) | 180 Ω → 180 Ω → bod A na breadboardu |
| pin 11 (GPIO17) | bod A |
| bod A | kondenzátor 100 nF → pin 9 (GND, −) |
| pin 32 (GPIO12) | 180 Ω → LED1 (+), dlouhá nožička |
| LED1 (−), krátká nožička | pin 34 (GND) |
| pin 33 (GPIO13) | 180 Ω → LED2 (+), dlouhá nožička |
| LED2 (−), krátká nožička | pin 34 (GND) |

Druhý krajní vývod potenciometru zůstává nezapojený, potenciometr tu funguje jako proměnný odpor.
Čísla pinů v tabulce jsou **fyzická**, program používá čísla **BCM GPIO** v závorkách.
Oba odpory 180 Ω chrání GPIO17, když program vybíjí kondenzátor a potenciometr je stažený na nulu.

Program nastaví GPIO17 na 0 a vybije kondenzátor. Pak pin přepne na vstup a měří, za kolik mikrosekund se objeví logická 1.
U našich součástek to vychází zhruba od 30 µs do 680 µs. Jednotlivá měření občas ujedou, proto program měří 9× a bere prostřední hodnotu (medián).
Jas LED řídí PWM s frekvencí 500 Hz.

Program [main.cpp](main.cpp) je v C++ a GPIO ovládá knihovnou `lgpio`. Na Raspberry Pi ji doinstalujeme, přeložíme a spustíme:

```sh
sudo apt install liblgpio-dev
g++ -O2 main.cpp -llgpio -o analog-io
./analog-io
```

Program zároveň běží jako malý web na portu 8007: `GET /stav` vrátí hodnotu potenciometru, čas nabíjení a jas LED, `POST /pot/50` nastaví logický potenciometr.
Dashboard ([dashboard/index.html](../dashboard/index.html)) ukazuje jas LED a posuvníkem nahrazuje potenciometr; pohnutí skutečným potenciometrem vrátí řízení zpět jemu.
Vždy běží jen jedna úloha, takže před spuštěním zastav program úlohy 6. Program ukončíš pomocí Ctrl+C.
