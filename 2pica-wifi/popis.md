Dvě Pica W spolu mluví bezdrátově přes Wi-Fi.
Pico B vytvoří vlastní Wi-Fi síť `PicoLink` a Pico A se k ní připojí.
Po stisku tlačítka pošle Pico A přes UDP na adresu 192.168.4.1, port 5005, písmeno „T“; Pico B ho přijme a přepne LED.

Pico A má program [WiFi.py](WiFi.py). Mezi Picy nevede žádný vodič, každé má vlastní USB napájení.

```text
Pico A
pin 19 (GP14) ── tlačítko ── pin 18 (GND / −)
```

Čísla pinů Pica v zapojení jsou **fyzická**, v programu `Pin(...)` používá číslo **GP**.
