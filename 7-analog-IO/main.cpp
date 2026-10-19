#include <lgpio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <algorithm>
#include <atomic>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <thread>

using namespace std::chrono;

// Cisla BCM GPIO, ne fyzicka cisla pinu konektoru.
const int RC = 17;
const int LED1 = 12;
const int LED2 = 13;

// Doba nabijeni kondenzatoru v mikrosekundach na krajich potenciometru.
const int CAS_MIN = 30;
const int CAS_MAX = 680;

int h;

// Stav sdileny mezi hlavni smyckou a webem pro dashboard (hodnoty 0 az 100).
std::atomic<int> potenciometr(0);
std::atomic<int> cas(0);
std::atomic<int> jas1(0);
std::atomic<int> jas2(0);
std::atomic<int> logicky(-1);  // -1 = dashboard nic nenastavil

// Vybije kondenzator a zmeri, za kolik mikrosekund se nabije na logickou 1.
int zmer_cas() {
    lgGpioClaimOutput(h, 0, RC, 0);
    std::this_thread::sleep_for(milliseconds(1));
    lgGpioClaimInput(h, 0, RC);
    auto zacatek = steady_clock::now();
    while (lgGpioRead(h, RC) == 0 && steady_clock::now() - zacatek < milliseconds(5)) {
    }
    return duration_cast<microseconds>(steady_clock::now() - zacatek).count();
}

// GET /stav vrati stav jako JSON, POST /pot/50 nastavi logicky potenciometr.
void web() {
    int server = socket(AF_INET, SOCK_STREAM, 0);
    int ano = 1;
    setsockopt(server, SOL_SOCKET, SO_REUSEADDR, &ano, sizeof(ano));
    sockaddr_in adresa = {};
    adresa.sin_family = AF_INET;
    adresa.sin_port = htons(8007);
    bind(server, (sockaddr*)&adresa, sizeof(adresa));
    listen(server, 5);

    while (true) {
        int spojeni = accept(server, nullptr, nullptr);
        char pozadavek[1024] = {};
        read(spojeni, pozadavek, sizeof(pozadavek) - 1);

        if (strncmp(pozadavek, "POST /pot/", 10) == 0) {
            logicky = std::clamp(atoi(pozadavek + 10), 0, 100);
        }

        std::string json = "{\"potenciometr\":" + std::to_string(potenciometr) +
                           ",\"cas\":" + std::to_string(cas) +
                           ",\"led1\":" + std::to_string(jas1) +
                           ",\"led2\":" + std::to_string(jas2) +
                           ",\"logicky\":" + (logicky >= 0 ? "true" : "false") + "}";
        std::string odpoved = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
                              "Access-Control-Allow-Origin: *\r\nContent-Length: " +
                              std::to_string(json.size()) + "\r\nConnection: close\r\n\r\n" + json;
        write(spojeni, odpoved.c_str(), odpoved.size());
        close(spojeni);
    }
}

int main() {
    h = lgGpiochipOpen(0);
    lgGpioClaimOutput(h, 0, LED1, 0);
    lgGpioClaimOutput(h, 0, LED2, 0);

    // Web bezi ve vlastnim vlakne, aby nezdrzoval mereni.
    std::thread(web).detach();

    int posledni_fyzicky = -1;

    while (true) {
        // Jednotliva mereni obcas ujedou (sum, zdrzeni Linuxem).
        // Zmerime 9x, seradime a vezmeme prostredni hodnotu (median).
        int mereni[9];
        for (int i = 0; i < 9; i++) {
            mereni[i] = zmer_cas();
        }
        std::sort(mereni, mereni + 9);
        int t = mereni[4];
        int fyzicky = std::clamp((t - CAS_MIN) * 100 / (CAS_MAX - CAS_MIN), 0, 100);

        // Pohnuti skutecnym potenciometrem zrusi hodnotu z dashboardu.
        if (posledni_fyzicky >= 0 && abs(fyzicky - posledni_fyzicky) > 3) {
            logicky = -1;
        }
        if (logicky < 0) {
            posledni_fyzicky = fyzicky;
        }
        int hodnota = logicky >= 0 ? logicky.load() : fyzicky;

        // Prvni polovina rozsviti LED1, druha polovina LED2.
        int novy1 = std::min(hodnota * 2, 100);
        int novy2 = std::max(hodnota * 2 - 100, 0);
        if (novy1 != jas1 || novy2 != jas2) {
            lgTxPwm(h, LED1, 500, novy1, 0, 0);
            lgTxPwm(h, LED2, 500, novy2, 0, 0);
        }

        potenciometr = hodnota;
        cas = t;
        jas1 = novy1;
        jas2 = novy2;

        std::this_thread::sleep_for(milliseconds(20));
    }
}
