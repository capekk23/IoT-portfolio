Dvě Pica W spolu mluví bezdrátově přes Wi-Fi.
Pico B vytvoří vlastní Wi-Fi síť `PicoLink` a Pico A se k ní připojí.
Po stisku tlačítka pošle Pico A přes UDP na adresu 192.168.4.1, port 5005, písmeno „T“; Pico B ho přijme, přepne LED na desce a krátce pípne.

Pico A má program [WiFi_A.py](WiFi_A.py), Pico B program [WiFi_B.py](WiFi_B.py).
Mezi Picy nevede žádný vodič, každé má vlastní USB napájení. Jako LED slouží zelená LED přímo na desce Pica B.

```text
Pico A
pin 19 (GP14) ── tlačítko ── pin 18 (GND / −)

Pico B
pin 20 (GP15) ── bzučák (+)   (aktivní bzučák)
pin 18 (GND / −) ── bzučák (−)
```

Čísla pinů Pica v zapojení jsou **fyzická**, v programu `Pin(...)` používá číslo **GP**.
