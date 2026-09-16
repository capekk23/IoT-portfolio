# IoT-portfolio
IoT projekty Karla Čapka ze 4.EP

Tři úlohy pro **Raspberry Pi Pico WH (RP2040, 2022)** v MicroPythonu.
Každá složka obsahuje jeden samostatný `main.py`, krátký `popis.md`
a složku `fotky/` pro skutečnou fotku zapojení.

| Úloha | Vstup → výstup | Dokumentace |
| --- | --- | --- |
| Digitální | Tlačítko → LED | [digi/popis.md](digi/popis.md) |
| Analogová | Potenciometr → jas LED (PWM) | [analog/popis.md](analog/popis.md) |
| Sběrnice | DS18B20 (1-Wire) → MAX7219 (SPI), podmíněně | [sbernice/popis.md](sbernice/popis.md) |

První dvě úlohy využívají uvedené součástky. U třetí je třeba ověřit
logické úrovně MAX7219; displej je proto v kódu zatím vypnutý. Pro
zamýšlené **I²C + SPI současně** nemáme potvrzenou I²C periferii: LCD
nemá I²C adaptér a bezdrátové moduly nejsou identifikované. Aktuální kód
proto používá variantu 1-Wire + SPI a I²C neimplementuje.

## Spuštění

1. Do desky nahrajte [MicroPython firmware pro Pico W](https://micropython.org/download/RPI_PICO_W/)
   (Pico WH má stejné MCU a firmware jako Pico W).
2. Zapojte jednu úlohu podle jejího popisu při odpojeném napájení.
   `GP` označuje číslo GPIO, čísla fyzických pinů jsou uvedena zvlášť.
3. V editoru s podporou MicroPythonu, například Thonny, otevřete příslušný
   `main.py` a spusťte jej na Picu. Pro automatický start soubor uložte
   do kořene úložiště Pica jako `main.py`; na desce běží vždy jedna úloha.
4. Doplňte vlastní fotografii do `<úloha>/fotky/zapojeni.jpg` a proveďte
   kontrolu chování uvedenou v popisu. Fotky ani hardwarové ověření zatím
   nejsou součástí projektu.

Pico má 3,3V GPIO; nepřivádějte na ně 5 V. Pro první dvě úlohy je zvolená
externí červená LED se dvěma rezistory 180 Ω v sérii.

[Referenční dokumentace MicroPython pro RP2](https://docs.micropython.org/en/latest/rp2/quickref.html)
