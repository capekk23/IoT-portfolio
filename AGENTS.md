# Pravidla práce v tomto repozitáři

## Rozsah změn

- Měň jen soubory přímo potřebné pro aktuální zadání. Před úpravou stručně řekni, co budeš měnit.
- README neupravuj bez výslovného zadání. Nepřidávej vedlejší úklid, nové funkce ani další dokumentaci z vlastní iniciativy.
- Před úpravami přečti aktuální soubory a respektuj ruční změny uživatele. U popisů měň jen dotčené vysvětlení nebo zapojení, nepřepisuj celý text.
- Když uživatel chce jen odpověď, nic neupravuj. Další možné změny můžeš navrhnout, ale neprováděj je bez zadání.

## Kód

- Piš co nejjednodušší funkční MicroPython, srozumitelný studentovi. Preferuj nastavení pinů a hlavní smyčku.
- Nepřidávej zbytečné třídy, obalové funkce, kontroly, ošetřování chyb, logování ani úklid při ukončení.
- Nezkracuj kód na úkor čitelnosti. Funkce použij tam, kde skutečně zjednoduší opakovanou práci, například přenos do displeje.
- Zachovej časování a kroky nutné pro funkci hardwaru, například čekání na měření nebo puštění tlačítka.
- Pro každou úlohu jeden samostatný `.py` soubor, zpravidla `main.py`. Zbytečně nepřidávej knihovny ani další soubory.
- Ověřuj kompatibilitu s MicroPythonem na Picu; úspěšná kontrola syntaxe v běžném Pythonu není důkaz funkčnosti na desce.

## Popisy a zapojení

- Piš česky, krátce a běžnými slovy, bez složitého vyjadřování.
- `popis.md` začíná přibližně třemi jednoduchými větami: co řešíme a jak. Pokud nestačí, přidej jen nezbytné vysvětlení.
- Pod popis patří jednoduché textové zapojení: vodiče, +, −, rezistory a čísla pinů.
- V zapojení uváděj fyzická čísla pinů Pica a GP v závorce. V kódu používá `Pin(...)` číslo GP. Tento rozdíl musí být jasný.
- Piny, napájení a zapojení kontroluj proti dokumentaci skutečné desky a dílů. Nezaměňuj podobné moduly a neoznačuj odhad za ověřený údaj.
- Když typ dílu není známý a ovlivňuje zapojení, vyžádej si jeho označení nebo popisky pinů.
- Fotky zapojení patří do složky úlohy, aktuálně do `fotky/`. Nevytvářej náhradní obrázky vydávané za skutečné zapojení.

## Spolupráce a ladění

- Komunikuj přímo a stručně. U běžné práce v zadaném rozsahu nevyžaduj opakovaná potvrzení.
- Při hlášené chybě nejdřív využij dostupný přístup k souborům, editoru a konzoli. Pokud je dostupné Thonny, zkus přečíst chybu tam místo okamžité žádosti o její přepsání.
- Nepředstírej přístup k videu, zapojení ani fyzickému displeji, pokud je skutečně nevidíš.
- Rozlišuj kontrolu syntaxe, běh na Picu a ověření skutečného chování zapojení. Oznamuj jen to, co bylo opravdu ověřeno.

## Výchozí podmínky

- Deska: Raspberry Pi Pico WH (RP2040, 2022), MicroPython.
- Jde o školní úlohy, ne produkční software. Prioritou je jednoduché a funkční řešení.
- Používej dostupné součástky; další nákupy nepředpokládej. Počítej s omezeným počtem vodičů a místem na breadboardu.
- Aktuální složky jsou `digi/`, `analog/` a `sbernice/`. Konkrétní stav a zapojení vždy zjisti z aktuálních souborů.
