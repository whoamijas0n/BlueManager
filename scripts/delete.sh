echo ""
echo -e "\033[32m[-] Lista de dispositivos emparejados\033[0m"
echo""
bluetoothctl power on
echo ""
bluetoothctl devices
echo ""
read -p $'\e[33m[-] Escriba la direccion MAC correspondiente el dispositivo que quiere eliminar \e[0m ' deletemac
echo ""
bluetoothctl remove $deletemac
echo ""
clear
echo -e "\033[32m[-] Operacion Completada\033[0m"