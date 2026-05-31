import subprocess
import re
from collections import Counter, defaultdict
from datetime import datetime
import speedtest

REPORT_FILE = "wifi_report.txt"


def run_command(command):
    try:
        return subprocess.check_output(
            command,
            shell=True,
            text=True,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        return ""


def get_wifi_info():
    output = run_command("iwconfig")

    ssid = re.search(r'ESSID:"(.+?)"', output)
    frequency = re.search(r'Frequency:(.+?) ', output)
    bitrate = re.search(r'Bit Rate=(.+?) ', output)
    signal = re.search(r'Signal level=(-\d+) dBm', output)

    return {
        "SSID": ssid.group(1) if ssid else "Brak",
        "Frequency": frequency.group(1) if frequency else "Brak",
        "BitRate": bitrate.group(1) if bitrate else "Brak",
        "Signal": signal.group(1) + " dBm" if signal else "Brak"
    }


def scan_networks():
    output = run_command("nmcli -t -f SSID dev wifi")

    networks = set()

    for line in output.splitlines():
        if line.strip():
            networks.add(line.strip())

    return sorted(networks)


def ping_test():
    output = run_command("ping -c 4 8.8.8.8")

    match = re.search(r'=\s[\d\.]+/([\d\.]+)/', output)

    if match:
        return match.group(1) + " ms"

    return "Brak danych"


def speed_test():
    st = speedtest.Speedtest()

    download = st.download() / 1_000_000
    upload = st.upload() / 1_000_000

    return {
        "download": round(download, 2),
        "upload": round(upload, 2),
        "ping": round(st.results.ping, 2)
    }


def analyze_wifi_interference():
    """
    Analiza zakłóceń kanałów Wi-Fi.
    Im większa suma sygnałów sieci na kanale,
    tym większe potencjalne zakłócenia.
    """

    output = run_command(
        "nmcli -t -f CHAN,SIGNAL dev wifi"
    )

    interference = defaultdict(float)

    for line in output.splitlines():

        try:
            channel, signal = line.split(":")
            channel = int(channel)
            signal = int(signal)

            interference[channel] += signal

        except ValueError:
            pass

    if not interference:
        return {}, None

    best_channel = min(
        interference,
        key=interference.get
    )

    return dict(interference), best_channel


def save_report(
        wifi_info,
        networks,
        ping,
        speed,
        interference,
        best_channel):

    with open(REPORT_FILE, "w", encoding="utf-8") as file:

        file.write("=== RAPORT ANALIZY WIFI ===\n")
        file.write(f"Data: {datetime.now()}\n\n")

        file.write("=== PARAMETRY WIFI ===\n")
        for key, value in wifi_info.items():
            file.write(f"{key}: {value}\n")

        file.write("\n=== DOSTĘPNE SIECI ===\n")
        for network in networks:
            file.write(f"- {network}\n")

        file.write("\n=== TEST PING ===\n")
        file.write(f"Średni ping: {ping}\n")

        file.write("\n=== TEST PRĘDKOŚCI ===\n")
        file.write(f"Download: {speed['download']} Mb/s\n")
        file.write(f"Upload: {speed['upload']} Mb/s\n")
        file.write(f"Ping: {speed['ping']} ms\n")

        file.write("\n=== ANALIZA KANAŁÓW WIFI ===\n")

        for channel, score in sorted(interference.items()):
            file.write(
                f"Kanał {channel}: "
                f"poziom zakłóceń = {score:.0f}\n"
            )

        if best_channel:
            file.write(
                f"\nRekomendowany kanał: "
                f"{best_channel}\n"
            )


def main():

    print("=== ANALIZA DOMOWEJ SIECI WIFI ===\n")

    print("Pobieranie parametrów Wi-Fi...")
    wifi_info = get_wifi_info()

    print("Skanowanie dostępnych sieci...")
    networks = scan_networks()

    print("Test ping...")
    ping = ping_test()

    print("Test prędkości Internetu...")
    speed = speed_test()

    print("Analiza zakłóceń kanałów Wi-Fi...")
    interference, best_channel = (
        analyze_wifi_interference()
    )

    print("\n=== WYNIKI ANALIZY KANAŁÓW ===")

    for channel, score in sorted(interference.items()):
        print(
            f"Kanał {channel}: "
            f"zakłócenia = {score:.0f}"
        )

    if best_channel:
        print(
            f"\nNajlepszy kanał: "
            f"{best_channel}"
        )

    save_report(
        wifi_info,
        networks,
        ping,
        speed,
        interference,
        best_channel
    )

    print(
        f"\nRaport zapisano do pliku: "
        f"{REPORT_FILE}"
    )


if __name__ == "__main__":
    main()