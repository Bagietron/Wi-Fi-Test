# Wi-Fi-Test
Program do analizy sieci Wi-Fi 

Program jest do użycia na systemie operacyjnym:
(Linux Mint 22.1 Cinnamon ver. 6.4.8)
(Kernel: 6.8.0-88 generic)

Do poprawnego działania należy zrobić aktualizacje i zainstalować pakiety:
- sudo apt update
- sudo apt install python3-pip
- sudo apt install network-manager
- sudo apt install wireless-tools
- sudo apt install net-tools
- sudo apt install speedtest-cli

Plik "wi-fi_analyzer.py" zapisać w folderze i przez terminal wejść w ten folder ('cd') oraz uruchomić program poprzez komendę "python3 wifi_analyzer.py".

W plikach txt są przykładowe pomiary z mojej sieci domowej. W pierwszym raporcie testuje połączenie z mojego pokoju, daleko od routera a w drugim dokładnie obok routera w salonie gdzie jest dużo urządzeń połączonych z routerem.

Niektóre różnice same się tłumaczą jak Download, upload i Siła sygnalu. Lecz wytłumaczę Ping, zakłócenia, częstotliwość oraz BitRate.

Ping - Nie ma zbyt istotnej różnicy co mogłoby się wydawać dziwne lecz jest całkowicie normalne gdyż upload jak i download spada to ping zostaje ten sam, ponieważ nie gubi pakietów. Gdybym oddalił sie jeszcze dalej ping zacząłby drastycznie skakać do 200ms

Zakłócenia - Przy routerze jest więcej zakłóceń niż w moim pokoju co też może niektórym sprawiać kłopoty dlaczego ale też jest proste wytłumaczenie, a powodem są inne urządzenia które są połączone z danym routerem (NIE JEST TO STANDARDOWY PARAMETR IEEE) i im bliżej routera tym więcej odbiera szumu od innych urządzeń, jest to tylko prosty wskaźnik zajętości kanału oparty na sumie sił wykrytych sieci Wi-Fi.

BitRate - To w skrócie ilość danych przesyłana przez łącze w ciagu jednej sekundy, u mnie to max 300 więc mam Wi-Fi 4

