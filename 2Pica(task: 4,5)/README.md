# Přetahovaná dvou Pic – úkoly 4 a 5

Každý hráč má Pico WH, tlačítko a osmipixelový kroužek RAINBOW-8 V1.2.
Klikáním rozšiřuje svoji barvu a přetlačuje druhého hráče; oba kroužky ukazují stejnou hru.
Stisky z Pica 2 putují drátem přes UART do Pica 1, které počítá hru a přes Wi-Fi posílá barvy zpět.

## Součástky

- 2× Raspberry Pi Pico WH s MicroPythonem pro **Pico W**.
- 2× RAINBOW-8 V1.2, osm RGB LED, vývody **G, V, DI**.
- 2× tlačítko, 4× rezistor 180 Ω, vodiče a breadboardy.
- 2× USB kabel pro napájení a nahrání programů.

Zapojení níže počítá s **3,3 V na V kroužku podle vašeho potvrzení pro používané kusy**.
Není to obecné tvrzení, že všechny kroužky WS2812B podporují napájení 3,3 V.
Program počítá s RGB kroužkem kompatibilním s NeoPixel/WS2812B, nikoli RGBW.

## Fyzické zapojení

Zapojovat bez USB. U obou Pic jsou čísla níže **fyzická čísla pinů**, číslo GP je v závorce.
V programu `Pin(...)` používá číslo **GP**.
Při pohledu ze strany součástek, s USB nahoře, je pin 1 vlevo nahoře a pin 40 vpravo nahoře.

### Pico 1 – červený hráč

```text
Pico 1                                   Kroužek 1
pin 36 (3V3 OUT / +3,3 V) ─────────────── V
pin 38 (GND / −) ─────────────────────── G
pin 20 (GP15) ── 180 Ω ── 180 Ω ─────── DI

Pico 1                                   Tlačítko 1
pin 19 (GP14) ─────────── tlačítko ────── pin 18 (GND / −)
```

### Pico 2 – modrý hráč

```text
Pico 2                                   Kroužek 2
pin 36 (3V3 OUT / +3,3 V) ─────────────── V
pin 38 (GND / −) ─────────────────────── G
pin 20 (GP15) ── 180 Ω ── 180 Ω ─────── DI

Pico 2                                   Tlačítko 2
pin 19 (GP14) ─────────── tlačítko ────── pin 18 (GND / −)
```

Dva rezistory 180 Ω jsou za sebou, celkem 360 Ω, v datovém vodiči poblíž DI.
Kroužek má vlastní řízení LED, jednotlivé LED další rezistory nepotřebují.
Tlačítko používá vnitřní přitahovací rezistor Pica. U čtyřnohého tlačítka vyber dva vývody, které se spojí až stiskem.

### Drát mezi Picy – UART

```text
Pico 2                                   Pico 1
pin 1 (GP0 / UART0 TX) ───────────────── pin 2 (GP1 / UART0 RX)
pin 3 (GND / −) ──────────────────────── pin 3 (GND / −)
```

Směr dat je **Pico 2 → Pico 1**. Zpětný UART vodič není potřeba.
Pin 1 Pica 1 a pin 2 Pica 2 zůstávají volné, přestože program nastavuje oba směry UART.
Každé Pico napájej vlastním USB. Napájecí piny 36 ani 40 mezi Picy nepropojuj; společná je pouze zem.
V tomto zapojení nepřipojuj V kroužku na 5 V: jeho DI dostává signál 3,3 V přímo z Pica.
Jas je omezený na `JAS = 24` z 255; při napájení z 3V3 ho ponech nízký.

## Nahrání a spuštění

1. Do **Pica 1** nahraj soubor [Pico 1/main.py](<Pico 1/main.py>) jako `main.py` do kořene desky.
2. Do **Pica 2** nahraj soubor [Pico 2/main.py](<Pico 2/main.py>) jako `main.py` do kořene desky.
3. Použij MicroPython pro Pico W, verzi **1.26.0 nebo novější**. Další knihovny se nekopírují.
4. Spusť Pico 1 a potom Pico 2. Při nahrávání v Thonny ověř, kterou desku máš vybranou.
5. Pico 1 vytvoří otevřenou Wi-Fi síť `Pico-pretahovana`. Pico 2 se připojí automaticky, bez hesla, routeru a internetu.
6. Do spojení jsou kroužky zhasnuté. Jakmile Pico 2 požádá o první obraz, objeví se červený a modrý bod a můžete hrát.

Oba kroužky polož stejně natočené. Pixel 0 je červený start, pixel 4 modrý start; fyzickou polohu pixelu 0 uvidíš po spuštění.
Pokud vedle sebe běží více dvojic, změň název Wi-Fi v obou programech jedné dvojice na stejný jedinečný název.

## Pravidla hry

- Pico 1 je červené, Pico 2 modré. Držení tlačítka přidá jen jeden stisk, další vyžaduje puštění.
- Zpočátku má každý jeden bod naproti druhému. Každých pět stisků rozšíří jeho barvu o pixel na obě strany; mezikroky se postupně rozjasňují.
- Po celkem 20 stiscích obou hráčů je kroužek zaplněný a hranice barev se posouvají podle rozdílu stisků. Na hranici se červená s modrou míchají do fialové.
- Náskok 20 stisků znamená výhru. Oba kroužky svítí tři sekundy barvou vítěze a pak začne nové kolo. Stisky během výhry se zahazují.
- Při stejném tempu se náskok nemění; kdo kliká rychleji, posouvá barvu k soupeřovu startu.

## Co přenášejí jednotlivá spojení

**Úkol 4 – drát:** UART0, 9600 baud, 8 datových bitů, bez parity, 1 stop bit.
Pico 2 po každém stisku pošle bajt `B`. Pico 1 čte vlastní tlačítko přímo a přičítá přijaté stisky soupeři.

**Úkol 5 – bezdrát:** Wi-Fi a UDP na portu 5000. Pico 1 má adresu `192.168.4.1`.
Pico 2 každých 50 ms pošle požadavek `?` a Pico 1 odpoví 24 bajty: osm trojic R, G, B.
Pico 2 zobrazí přijaté barvy. Přenos má malé zpoždění, nejde o přesně současné rozsvícení obou kroužků.
Ztracený UDP obrázek nahradí další; po restartu desky nebo přerušení spojení restartuj obě Pica pro nové kolo.

## Ověření na stole

Po nahrání vyzkoušej obě tlačítka: červené i modré stisky musí měnit oba kroužky stejně, držení nesmí dál přičítat.
Potom nech jednoho hráče získat 20 stisků náskoku a ověř výhru i nové kolo.
Pro ukázku UART odpoj pouze signál TX → RX: modré stisky se přestanou počítat, ale obraz se přes Wi-Fi dál přenáší.
Před dalším kolem vodič vrať a restartuj obě desky.

Zdrojáky používají rozhraní dostupná v MicroPythonu pro RP2040/Pico W.
Na počítači prošla kontrola syntaxe a simulace obou programů: zákmit a držení tlačítka, přenos stisků, obnova ztraceného obrázku, výhra obou hráčů a nové kolo.
Běh na skutečných deskách, barvy a spolehlivost konkrétních kroužků při 3,3 V je potřeba ověřit na vašem zapojení.

## Podklady

- [Fyzické piny Pico W/WH](https://datasheets.raspberrypi.com/picow/PicoW-A4-Pinout.pdf).
- [MicroPython 1.26.0 pro RP2 – UART, Wi-Fi a NeoPixel](https://docs.micropython.org/en/v1.26.0/rp2/quickref.html).
- [Adafruit – napájení a datové úrovně NeoPixelů](https://learn.adafruit.com/adafruit-neopixel-uberguide/powering-neopixels).
