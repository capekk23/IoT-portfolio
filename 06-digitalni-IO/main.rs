use rppal::gpio::Gpio;
use std::io::{Read, Write};
use std::net::TcpListener;
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::sync::Arc;
use std::thread::{sleep, spawn};
use std::time::{Duration, Instant};

// Cas mezi prohozenim LED, v milisekundach.
const INTERVALY: [u64; 6] = [100, 250, 500, 1000, 1500, 2000];

// Stav sdileny mezi hlavni smyckou a webem pro dashboard.
struct Stav {
    rychlost: AtomicUsize,
    led1: AtomicBool,
    logicke_tlacitko: AtomicBool,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let gpio = Gpio::new()?;
    // Cisla BCM GPIO, ne fyzicka cisla pinu konektoru.
    let tlacitko = gpio.get(14)?.into_input_pullup();
    let mut led1 = gpio.get(15)?.into_output_high();
    let mut led2 = gpio.get(16)?.into_output_low();

    let stav = Arc::new(Stav {
        rychlost: AtomicUsize::new(0),
        led1: AtomicBool::new(true),
        logicke_tlacitko: AtomicBool::new(false),
    });

    // Web bezi ve vlastnim vlakne, aby nezdrzoval blikani.
    let web_stav = stav.clone();
    spawn(move || web(web_stav));

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
        let mut novy_stisk = false;
        if cteni != stisknuto && ted.duration_since(zmena_tlacitka) >= Duration::from_millis(30) {
            stisknuto = cteni;
            novy_stisk = stisknuto;
        }

        // Logicke tlacitko z dashboardu funguje stejne jako stisk skutecneho.
        if stav.logicke_tlacitko.swap(false, Ordering::Relaxed) {
            novy_stisk = true;
        }

        if novy_stisk {
            rychlost = (rychlost + 1) % INTERVALY.len();
            posledni_bliknuti = ted;
        }

        if ted.duration_since(posledni_bliknuti) >= Duration::from_millis(INTERVALY[rychlost]) {
            led1.toggle();
            led2.toggle();
            posledni_bliknuti = ted;
        }

        stav.rychlost.store(rychlost, Ordering::Relaxed);
        stav.led1.store(led1.is_set_high(), Ordering::Relaxed);

        sleep(Duration::from_millis(5));
    }
}

// GET /stav vrati stav jako JSON, POST /tlacitko stiskne logicke tlacitko.
fn web(stav: Arc<Stav>) {
    let server = TcpListener::bind("0.0.0.0:8006").unwrap();
    for spojeni in server.incoming() {
        let mut spojeni = spojeni.unwrap();
        let mut pozadavek = [0; 1024];
        let _ = spojeni.read(&mut pozadavek);

        if pozadavek.starts_with(b"POST /tlacitko") {
            stav.logicke_tlacitko.store(true, Ordering::Relaxed);
        }

        let led1 = stav.led1.load(Ordering::Relaxed);
        let json = format!(
            "{{\"led1\":{},\"led2\":{},\"interval\":{}}}",
            led1,
            !led1,
            INTERVALY[stav.rychlost.load(Ordering::Relaxed)]
        );
        let odpoved = format!(
            "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{}",
            json.len(),
            json
        );
        let _ = spojeni.write_all(odpoved.as_bytes());
    }
}
