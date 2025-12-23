# BlueManager
BlueManager es una interfaz simplificada por consola (TUI) escrita en Bash para gestionar dispositivos Bluetooth en sistemas Linux. Utiliza bluetoothctl para realizar tareas como escaneo, emparejamiento y conexión de forma rápida y visual.

<p align="center">
  <img src="img/menu.jpeg" alt="Imagen de el menu de BlueManager" width="850">
</p>

## Requisitos e Instalación
Para que el script funcione correctamente, es necesario tener instalado el paquete bluez y que el servicio de Bluetooth esté activo.
```text
+------------------------+---------------------------------------------+
| Distribución           | Comando de Instalación                      |
+------------------------+---------------------------------------------+
| Arch Linux / Manjaro   | sudo pacman -S bluez bluez-utils            |
+------------------------+---------------------------------------------+
| Debian / Ubuntu / Kali | sudo apt update && sudo apt install bluez   |
+------------------------+---------------------------------------------+
| Fedora                 | sudo dnf install bluez bluez-tools          |
+------------------------+---------------------------------------------+
```
### Clonar y configurar
```bash
# Clonar el repositorio
git clone https://github.com/whoamijas0n/BlueManager.git
cd BlueManager

# Dar permisos de ejecución a los scripts
chmod +x bluemana.sh scripts/*.sh
```
[!IMPORTANT] Asegúrate de que el servicio de bluetooth esté corriendo antes de iniciar: sudo systemctl start bluetooth
## Uso
Para iniciar la herramienta, simplemente ejecuta el script principal desde la raíz del proyecto:
```bash
bash bluemana.sh
```
## Licencia y Autor
Este proyecto ha sido creado por **Jason Caballero (whoamijas0n)**.
Distribuido bajo la licencia **GNU General Public License v3.0**.  
Consulta el archivo `LICENSE` para más detalles.

