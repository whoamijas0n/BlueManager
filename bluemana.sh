clear

# empieza el bucle, hasta que el usuario seleccione la opcion numero 1 el menu se va a repetir

until [ "$opcion" = "0" ]
do

# se ejecuta el script para el logo y informacion de el programa

bash scripts/log.sh


# menu de opciones para seleccionar la accion que se desea llevar a cabo

echo ""
echo -e "\033[33m[-] Menu de opciones:\033[0m"
echo ""
echo "[1] Emparejar un dispositivo"
echo "[2] Conectarse a un dispositivo"
echo "[3] Eliminar un dispositivo"
echo "[4] Desconectarse a un dispositivo"
echo "[5] Lista de dispositivos emparejados"
echo "[0] Salir"
echo ""

read -p $'\e[31m[-] Elige una opcion: \e[0m ' opcion

# empieza el menu de casos segun la opcion que se haya tomado

case $opcion in

	"0")
		echo ""
		echo -e "\033[32m[!] Saliendo de el programa ¡Gracias por usar BlueManager!\033[0m"
		echo ""
	;;

	"1")
		bash scripts/pair.sh
		;;

	"2")
		bash scripts/connect.sh
		;;

	"3")
		clear
		bash scripts/delete.sh
		;;

	"4")
		clear
		bash scripts/disconnect.sh
		;;

	"5")
		echo ""
    	echo -e "\033[32m[!] Dispositivos emparejados:\033[0m"
        echo ""
        bluetoothctl devices
        echo ""
        read -p $'\e[33m[-] Presioe ENTER para continuar \e[0m ' ENTER
        clear

	;;
	
	*)
		clear
		echo -e "\033[31m[!] Opcion invalida, repita denuevo.\033[0m"
	;;

# Termina el menu de casos
esac	

# termina el bucle de el menu principal
done
