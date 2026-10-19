use rppal::gpio::Gpio;
use std::thread::sleep;
use std::time::{Duration, Instant};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let gpio = Gpio::new()?;
    // Cisla BCM GPIO, ne fyzicka cisla pinu konektoru.
    let tlacitko = gpio.get(14)?.into_input_pullup();
    let mut led1 = gpio.get(15)?.into_output_high();
    let mut led2 = gpio.get(16)?.into_output_low();

    // Cas mezi prohozenim LED, v milisekundach.
    let intervaly = [100, 250, 500, 1000, 1500, 2000];
    let mut rychlost = 0;
    let mut posledni_bliknuti = Instant::now();
    let mut posledni_cteni = tlacitko.is_low();
    let mut stisknuto = posledni_cteni;
    let mut zmena_tlacitka = Instant::now();

    loop {
        let ted = Instant::now();
        let cteni = tlacitko.is_low();

        if cteni != posledni_cteni {
            posledni_cteni = cteni;
            zmena_tlacitka = ted;
        }

        // Zmenu prijmeme po 30 ms stabilniho stavu (potlaceni zakmitu).
        if cteni != stisknuto && ted.duration_since(zmena_tlacitka) >= Duration::from_millis(30) {
            stisknuto = cteni;
            if stisknuto {
                rychlost = (rychlost + 1) % intervaly.len();
                posledni_bliknuti = ted;
            }
        }

        if ted.duration_since(posledni_bliknuti) >= Duration::from_millis(intervaly[rychlost]) {
            led1.toggle();
            led2.toggle();
            posledni_bliknuti = ted;
        }

        sleep(Duration::from_millis(5));
    }
}
