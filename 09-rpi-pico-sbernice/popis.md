Raspberry Pi 4 a Pico spolu mluví po sběrnici I2C. Pi je controller, Pico je target na adrese 0x42.
Po stisku tlačítka na Pi pošle Pi na Pico písmeno „T“; Pico přepne LED a krátce pípne.
Pi pak z Pica po stejné sběrnici přečte, jestli LED svítí, a ukáže to na dashboardu. Dashboard má i logické tlačítko.

| Odkud | Kam |
|---|---|
| Pi pin 3 (GPIO2, I2C SDA) | Pico pin 1 (GP0, I2C0 SDA) |
| Pi pin 5 (GPIO3, I2C SCL) | Pico pin 2 (GP1, I2C0 SCL) |
| Pi pin 9 (GND) | Pico pin 3 (GND) |
| Pi pin 11 (GPIO17) | tlačítko → Pi pin 14 (GND) |
| Pico pin 19 (GP14) | 180 Ω → 180 Ω → LED (+), dlouhá nožička |
| LED (−), krátká nožička | Pico pin 18 (GND) |
| Pico pin 20 (GP15) | bzučák (+) (aktivní bzučák) |
| bzučák (−) | Pico pin 23 (GND) |

U I2C se vodiče nekříží: SDA vede na SDA a SCL na SCL. Země Pi a Pica musí být propojené.
Pico napájej vlastním USB (třeba z USB portu Pi). Napájecí piny 3,3 V ani 5 V mezi Pi a Picem nepropojuj.
Pull-up rezistory na SDA a SCL už má Pi na desce, na 3,3 V, takže pro Pico jsou v pořádku.
Čísla pinů v tabulce jsou **fyzická**. Pi v programu používá čísla **BCM GPIO**, Pico v `Pin(...)` čísla **GP**.

Na Pico nahraj [pico.py](pico.py) jako `main.py`. Používá `machine.I2CTarget`, takže na Picu musí být MicroPython 1.25 nebo novější.

Na Pi běží [rpi.rb](rpi.rb) v Ruby. I2C ovládá přímo přes soubor `/dev/i2c-1`, tlačítko čte nástrojem `gpiomon`, žádné další knihovny nepotřebuje.
I2C musí být zapnuté (`sudo raspi-config nonint do_i2c 0`, jako u úlohy 8). Ruby nainstalujeme a program spustíme:

```sh
sudo apt install ruby
ruby rpi.rb
```

Program zároveň běží jako malý web na portu 8009: `GET /stav` vrátí stav LED přečtený z Pica a počet stisků, `POST /tlacitko` je logické tlačítko.
Vždy běží jen jedna úloha, před spuštěním zastav program úlohy 8. Program ukončíš pomocí Ctrl+C.
