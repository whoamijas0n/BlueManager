<div align = "center">

<img src="img/logo.png" alt="logo" width="800" height="auto" />


</div>
<br/>

`BlueManager` es una interfaz de usuario interactiva para la terminal (**TUI - Terminal User Interface**) reescrita completamente en **Python 3** y diseñada bajo el paradigma de programación orientada a objetos (POO) utilizando la librería estándar `curses`. 

Esta herramienta abstracta por completo la complejidad de interactuar manualmente con la utilidad de consola `bluetoothctl` (paquete *BlueZ*) en sistemas operativos Linux, proporcionando una experiencia fluida, automatizada y con un entorno visual monocromático/azul profundo de baja sobrecarga (*low-overhead*).

<p align="center">
  <strong>Moderno • Minimalista • Orientado a Objetos • Seguro</strong>
</p>

---

<div align = "center">

##  Características Clave

</div>

*   **Refactorización Completa a Python 3:** Se ha sustituido la antigua arquitectura basada en múltiples scripts dispersos de Bash (`bluemana.sh`, `scripts/*.sh`) por un único núcleo centralizado, limpio y mantenible (`main.py`).
*   **Interfaz de Terminal (TUI) Fluida:** Implementación nativa con la librería `curses`, que incluye soporte para temas personalizados con paletas profundas mediante manipulación directa de valores RGB (escala 0-1000).
*   **Splash Screen Animada:** Pantalla de carga dinámica con efectos cinéticos y atenuación de ruido visual aleatorio (`░▒▓█`) para una inmersión estética de estilo *Red Team / Cyberpunk*.
*   **Gestión de Dispositivos Dinámica y sin Entrada Manual:** Elimina la tediosa tarea de copiar y pegar o transcribir direcciones MAC. El script lee las salidas filtradas a través de expresiones regulares (`re`) e inyecta dinámicamente las llamadas (*callbacks*) en el alcance de ejecución (*scope closures*).
*   **Aislamiento y Concurrencia de Procesos:** Ejecución segura de comandos del sistema a través de la API nativa de `subprocess`, implementando manejadores de excepciones, capturas robustas de flujos de salida estándar (`stdout`/`stderr`), y mecanismos de control de temporización (*timeouts*).

---

<div align = "center">

##  Requisitos del Sistema

</div>

Para el correcto funcionamiento de `BlueManager`, asegúrate de cumplir con las siguientes dependencias del sistema:

1.  **Entorno Operativo:** GNU/Linux.
2.  **Lenguaje:** Python `3.x` (con soporte para el módulo integrado `curses`).
3.  **Subsistema de Bluetooth:** El paquete `bluez` instalado y el demonio/servicio activo.


### Instalación de dependencias por distribución


| Distribución | Comando de Instalación |
| :--- | :--- |
| **Arch Linux / Manjaro** | `sudo pacman -S bluez bluez-utils python` |
| **Debian / Ubuntu / Kali** | `sudo apt update && sudo apt install bluez python3` |
| **Fedora** | `sudo dnf install bluez bluez-tools python3` |

>  **Nota Crítica:** El servicio de Bluetooth debe estar activo antes de lanzar la aplicación. Puedes arrancarlo ejecutando:
> ```bash
> sudo systemctl start bluetooth
> ```

---

<div align = "center">

## Instalación y Configuración

</div>

Sigue estos sencillos pasos para clonar el repositorio y preparar el entorno de ejecución:

```bash
# 1. Clonar el repositorio oficial
git clone https://github.com/whoamijas0n/BlueManager.git
cd BlueManager

# 2. Conceder permisos de ejecución al script unificado
chmod +x main.py
```

---

<div align = "center">

## Modo de Uso

</div>

Dado que el proyecto ha sido consolidado en una arquitectura unificada de un solo script, su inicialización es directa e inmediata:

```bash
python3 main.py
```


### Controles de la Interfaz:
*   `↑` / `↓` : Navegar verticalmente por el menú adaptativo.
*   `ENTER` o `ESPACIO` : Seleccionar y ejecutar la acción actual.
*   `←` o `BACKSPACE` / `B` : Volver de manera segura al menú principal (desapilar menú).
*   `Q` : Terminar la aplicación limpiando el búfer de la terminal de forma segura.


