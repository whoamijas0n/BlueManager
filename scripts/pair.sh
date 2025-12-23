echo ""
echo -e "\033[32m[-] Lista de dispositivos disponibles\033[0m"
echo""
bluetoothctl power on
agent on
echo ""
bluetoothctl --timeout 10 scan on
echo ""
read -p $'\e[33m[-] Escriba la direccion MAC correspondiente el dispositivo que quiere emparejar \e[0m ' pairmac
echo ""
bluetoothctl pair $pairmac
echo ""
clear
echo -e "\033[32m[-] Operacion Completada\033[0m"