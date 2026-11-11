Chceme měřit vzdálenost ultrazvukovým senzorem HC-SR04 na Raspberry Pi 4 a ukazovat ji na dvou displejích.
LCD 16×2 přes sběrnici I2C ukazuje vzdálenost v cm, matice 8×8 s MAX7219 přes sběrnici SPI ukazuje blízkost předmětu.
Každý centimetr navíc zhasne jednu LED matice ve spirále od okraje ke středu: do 6 cm svítí celá, od 70 cm je zhasnutá.

| Odkud | Kam |
|---|---|
| pin 2 (5 V) | lišta + |
| pin 6 (GND) | lišta − |
| LCD VCC / GND | lišta + / lišta − |
| LCD SDA | pin 3 (GPIO2, I2C SDA) |
| LCD SCL | pin 5 (GPIO3, I2C SCL) |
| matice VCC / GND | lišta + / lišta − |
| matice DIN | pin 19 (GPIO10, SPI MOSI) |
| matice CLK | pin 23 (GPIO11, SPI SCLK) |
| matice CS | pin 24 (GPIO8, SPI CE0) |
| HC-SR04 VCC / GND | lišta + / lišta − |
| HC-SR04 Trig | pin 16 (GPIO23) |
| HC-SR04 Echo | 180 Ω → bod B |
| bod B | pin 18 (GPIO24) |
| bod B | 180 Ω → 180 Ω → lišta − |

Čísla pinů v tabulce jsou **fyzická**, program používá čísla **BCM GPIO** v závorkách.
Senzor potřebuje 5 V. Echo pak vrací 5 V, ale Pi snese jen 3,3 V, proto jsou na Echo tři rezistory 180 Ω jako dělič.
LCD je stejně jako u Pica na 5 V. Pin 1 (3,3 V) a pin 2 (5 V) nikdy nespojuj.
Když senzor nic nezachytí, drží Echo asi 200 ms v 1; program před dalším měřením počká, až Echo spadne na 0.

Program [Program.cs](Program.cs) je v C# a používá jen balíček `System.Device.Gpio` (GPIO, I2C a SPI). LCD i matici ovládá posíláním bajtů stejně jako úloha 3 na Picu.
Na Raspberry Pi zapneme I2C a SPI (`sudo raspi-config nonint do_i2c 0`, `sudo raspi-config nonint do_spi 0`, restart) a nainstalujeme .NET 10. Pak ve složce úlohy:

```sh
dotnet run -c Release
```

Program zároveň běží jako malý web na portu 8008: `GET /stav` vrátí vzdálenost, počet svítících LED a text LCD, `POST /vzdalenost/30` předstírá 30 cm na 3 s.
Dashboard ([dashboard/index.html](../dashboard/index.html)) ukazuje kopii LCD a matice a posuvníkem nahrazuje senzor.
Vždy běží jen jedna úloha. Program ukončíš pomocí Ctrl+C.

[Video zapojení](fotky/proof.mp4)
