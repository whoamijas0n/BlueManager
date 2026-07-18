#!/usr/bin/env python3
import curses
import subprocess
import os
import sys
import random
import time
import re

# Arte ASCII de BlueManager
ARTE_BLUEMANAGER = r"""
▄▄▄▄· ▄▄▌  ▄• ▄▌▄▄▄ .• ▌ ▄ ·.  ▄▄▄·  ▐ ▄  ▄▄▄·  ▄▄ • ▄▄▄ .▄▄▄  
┌█ ▀█▪██•  █▪██▌▀▄.▀··██ ▐███▪▐█ ▀█ •█▌▐█▐█ ▀█ ▐█ ▀ ▪▀▄.▀·▀▄ █·
▐█▀▀█▄██▪  █▌▐█▌▐▀▀▪▄▐█ ▌▐▌▐█·▄█▀▀█ ▐█▐▐▌▄█▀▀█ ▄█ ▀█▄▐▀▀▪▄▐▀▀▄ 
██▄▪▐█▐█▌▐▌▐█▄█▌▐█▄▄▌██ ██▌▐█▌▐█ ▪▐▌██▐█▌▐█ ▪▐▌▐█▄▪▐█▐█▄▄▌▐█•█▌
·▀▀▀▀ .▀▀▀  ▀▀▀  ▀▀▀ ▀▀  █▪▀▀▀ ▀  ▀ ▀▀ █▪ ▀  ▀ ·▀▀▀▀  ▀▀▀ .▀  ▀
"""

class Menu:
    def __init__(self, titulo):
        self.titulo = titulo
        self.opciones = []
        self.indice_actual = 0

    def agregar_opcion(self, nombre, destino):
        self.opciones.append((nombre, destino))


class BluetoothController:
    """Clase encargada de interactuar de forma segura con bluetoothctl mediante subprocess."""
    
    @staticmethod
    def ejecutar_comando(comando, timeout=None):
        """Ejecuta un comando en el sistema de manera segura."""
        try:
            resultado = subprocess.run(
                comando, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True, 
                timeout=timeout
            )
            return resultado.returncode, resultado.stdout, resultado.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Tiempo de espera agotado"
        except Exception as e:
            return -1, "", str(e)

    @classmethod
    def inicializar_bluetooth(cls):
        """Asegura el encendido del controlador y agente bluetooth de forma silenciosa."""
        cls.ejecutar_comando(['bluetoothctl', 'power', 'on'])
        cls.ejecutar_comando(['bluetoothctl', 'agent', 'on'])

    @classmethod
    def obtener_dispositivos_emparejados(cls):
        """Obtiene la lista de dispositivos emparejados en el sistema."""
        code, stdout, _ = cls.ejecutar_comando(['bluetoothctl', 'devices'])
        if code != 0:
            return []
        
        dispositivos = []
        # Expresión regular para parsear: Device MA:C_:AD:DR:ES:SS Nombre
        patron = re.compile(r'^Device\s+([0-9A-Fa-f:]{17})\s+(.*)$')
        for linea in stdout.strip().split('\n'):
            match = patron.match(linea.strip())
            if match:
                mac, nombre = match.groups()
                dispositivos.append({'mac': mac, 'nombre': nombre})
        return dispositivos

    @classmethod
    def escanear_dispositivos(cls):
        """Escanea dispositivos Bluetooth cercanos durante un tiempo límite (10s)."""
        # Se ejecuta un escaneo controlado similar al script original
        cls.ejecutar_comando(['bluetoothctl', '--timeout', '10', 'scan', 'on'])
        
        # Una vez escaneado, bluetoothctl guarda en caché los dispositivos encontrados.
        # Filtramos mediante 'bluetoothctl devices' que devuelve tanto emparejados como descubiertos.
        return cls.obtener_dispositivos_emparejados()


class AplicacionTUI:
    def __init__(self, stdscr, menu_raiz):
        self.stdscr = stdscr
        self.pila_menus = [menu_raiz]
        curses.curs_set(0)
        self.stdscr.keypad(True)
        curses.start_color()
        curses.use_default_colors()
        
        # Tema Azul
        curses.init_pair(1, curses.COLOR_BLUE, -1)
        try:
            # Cambiamos los valores RGB (escala 0 a 1000). 
            # 0 de Rojo, 150 de Verde y 650 de Azul para un tono elegante y profundo.
            curses.init_color(9, 0, 150, 650)
            curses.init_pair(2, 9, -1)
            self.color_principal = curses.color_pair(2)
        except curses.error:
            self.color_principal = curses.color_pair(1)

    def dibujar_interfaz(self):
        self.stdscr.clear()
        alto, ancho = self.stdscr.getmaxyx()
        color = self.color_principal
        
        if alto < 20 or ancho < 75:
            self.stdscr.addstr(alto // 2, max(0, (ancho // 2) - 11), "Terminal muy pequeña.", color)
            self.stdscr.refresh()
            return False

        self.stdscr.attron(color)
        self.stdscr.border(0, 0, 0, 0, 0, 0, 0, 0)
        self.stdscr.attroff(color)

        menu_actual = self.pila_menus[-1]
        arte_ascii = ARTE_BLUEMANAGER.strip('\n').split('\n')
        titulo = f"=== {menu_actual.titulo} ==="
        subtitulo = "[ ↑/↓: Navegar | ESPACIO/ENTER: Seleccionar | ←: Volver | Q: Salir ]"

        elementos_totales = len(arte_ascii) + 5 + len(menu_actual.opciones)
        y_inicial = (alto // 2) - (elementos_totales // 2)

        self.stdscr.attron(color)
        for i, linea in enumerate(arte_ascii):
            x = (ancho // 2) - (len(linea) // 2)
            try:
                self.stdscr.addstr(y_inicial + i, max(0, x), linea)
            except curses.error: pass
        self.stdscr.attroff(color)

        y_titulo = y_inicial + len(arte_ascii) + 2
        try:
            self.stdscr.addstr(y_titulo, (ancho // 2) - (len(titulo) // 2), titulo, curses.A_BOLD | curses.A_UNDERLINE | color)
            self.stdscr.addstr(y_titulo + 1, (ancho // 2) - (len(subtitulo) // 2), subtitulo, color)
        except curses.error: pass

        y_opciones = y_titulo + 3
        for i, (nombre, _) in enumerate(menu_actual.opciones):
            texto = f" {nombre} "
            x = (ancho // 2) - (len(texto) // 2 + 4)
            try:
                if i == menu_actual.indice_actual:
                    self.stdscr.addstr(y_opciones + i, max(0, x), f">>{texto}<<", curses.A_REVERSE | curses.A_BOLD | color)
                else:
                    self.stdscr.addstr(y_opciones + i, max(0, x), f"  {texto}  ", color)
            except curses.error: pass

        self.stdscr.refresh()
        return True

    def animar_splash_screen(self):
        arte_ascii = ARTE_BLUEMANAGER.strip('\n').split('\n')
        ruido_chars = ["░", "▒", "▓", "█", "#", "@", "%", "*"]
        frames_totales = 18
        
        for frame in range(frames_totales + 1):
            self.stdscr.clear()
            alto, ancho = self.stdscr.getmaxyx()
            if alto < 20 or ancho < 75: break
                
            self.stdscr.attron(self.color_principal)
            self.stdscr.border(0, 0, 0, 0, 0, 0, 0, 0)
            nivel_ruido = 1.0 - (frame / frames_totales)
            y_inicial = (alto // 2) - (len(arte_ascii) // 2)
            
            for i, linea in enumerate(arte_ascii):
                linea_borrosa = ""
                for char in linea:
                    if char not in (" ", "\n") and random.random() < nivel_ruido:
                        linea_borrosa += random.choice(ruido_chars)
                    else:
                        linea_borrosa += char
                x = (ancho // 2) - (len(linea_borrosa) // 2)
                try: self.stdscr.addstr(y_inicial + i, max(0, x), linea_borrosa)
                except curses.error: pass
                    
            self.stdscr.attroff(self.color_principal)
            self.stdscr.refresh()
            curses.napms(80)
        curses.napms(500)

    def mostrar_mensaje_popup(self, mensaje, es_error=False):
        """Muestra una ventana emergente/popup temporal con un mensaje centrado."""
        self.stdscr.clear()
        alto, ancho = self.stdscr.getmaxyx()
        
        self.stdscr.attron(self.color_principal)
        self.stdscr.border(0, 0, 0, 0, 0, 0, 0, 0)
        self.stdscr.attroff(self.color_principal)
        
        lineas = mensaje.split('\n')
        lineas.append("")
        lineas.append("[ Presione ENTER para continuar ]")
        
        y_centro = (alto // 2) - (len(lineas) // 2)
        for idx, linea in enumerate(lineas):
            x = (ancho // 2) - (len(linea) // 2)
            estilo = self.color_principal
            if idx == len(lineas) - 1:
                estilo |= curses.A_BLINK
            try:
                self.stdscr.addstr(y_centro + idx, max(0, x), linea, estilo)
            except curses.error: pass
            
        self.stdscr.refresh()
        
        # Esperar hasta presionar Enter
        while True:
            tecla = self.stdscr.getch()
            if tecla in [curses.KEY_ENTER, 10, 13]:
                break

    def ejecutar_accion_bluetooth(self, comando_base, mac, nombre_dispositivo):
        """Ejecuta una acción de bluetoothctl en segundo plano y despliega el feedback."""
        self.stdscr.clear()
        alto, ancho = self.stdscr.getmaxyx()
        msg_espera = f"Procesando: {comando_base.upper()} -> {nombre_dispositivo}..."
        try:
            self.stdscr.addstr(alto // 2, (ancho // 2) - (len(msg_espera) // 2), msg_espera, self.color_principal)
        except curses.error: pass
        self.stdscr.refresh()

        code, stdout, stderr = BluetoothController.ejecutar_comando(['bluetoothctl', comando_base, mac])
        
        if code == 0 and "fail" not in stdout.lower():
            msg_resultado = f"Operación Completada:\n{nombre_dispositivo} ({mac}) procesado con éxito."
            self.mostrar_mensaje_popup(msg_resultado)
        else:
            msg_error = f"Error al ejecutar {comando_base}:\n" + (stdout if stdout else stderr)
            self.mostrar_mensaje_popup(msg_error, es_error=True)

        # Regresa automáticamente eliminando el submenú dinámico de la pila
        if len(self.pila_menus) > 1:
            self.pila_menus.pop()

    def generar_menu_dispositivos(self, accion, escanear=False):
        """Genera dinámicamente el submenú con dispositivos disponibles sin requerir teclear MAC."""
        self.stdscr.clear()
        alto, ancho = self.stdscr.getmaxyx()
        msg = "Cargando lista de dispositivos Bluetooth..." if not escanear else "Escaneando dispositivos cercanos (10s)..."
        try:
            self.stdscr.addstr(alto // 2, (ancho // 2) - (len(msg) // 2), msg, self.color_principal | curses.A_BLINK)
        except curses.error: pass
        self.stdscr.refresh()

        # Asegurar conectividad antes de listar
        BluetoothController.inicializar_bluetooth()

        if escanear:
            dispositivos = BluetoothController.escanear_dispositivos()
        else:
            dispositivos = BluetoothController.obtener_dispositivos_emparejados()

        if not dispositivos:
            self.mostrar_mensaje_popup("No se encontraron dispositivos Bluetooth disponibles.")
            return

        nuevo_menu = Menu(f"{accion.capitalize()} Dispositivo")
        for disp in dispositivos:
            nombre_mostrar = f"{disp['nombre']} [{disp['mac']}]"
            # Inyección de callback dinámico vía clausura de scope
            nuevo_menu.agregar_opcion(
                nombre_mostrar, 
                lambda app, mac=disp['mac'], name=disp['nombre']: app.ejecutar_accion_bluetooth(accion, mac, name)
            )
        
        nuevo_menu.agregar_opcion("<< Volver al Menú Principal", "VOLVER")
        self.pila_menus.append(nuevo_menu)

    def mostrar_lista_emparejados(self):
        """Muestra los dispositivos emparejados en un popup temporal."""
        BluetoothController.inicializar_bluetooth()
        dispositivos = BluetoothController.obtener_dispositivos_emparejados()
        
        if not dispositivos:
            self.mostrar_mensaje_popup("No hay dispositivos emparejados.")
            return
            
        texto_dispositivos = "Dispositivos Emparejados:\n"
        for disp in dispositivos:
            texto_dispositivos += f"• {disp['nombre']} -> {disp['mac']}\n"
            
        self.mostrar_mensaje_popup(texto_dispositivos.strip())

    def ejecutar(self):
        self.animar_splash_screen()
        while True:
            espacio_suficiente = self.dibujar_interfaz()
            tecla = self.stdscr.getch()
            if not espacio_suficiente:
                if tecla in [ord('q'), ord('Q')]: break
                continue
            
            menu_actual = self.pila_menus[-1]
            if tecla == curses.KEY_UP and menu_actual.indice_actual > 0:
                menu_actual.indice_actual -= 1
            elif tecla == curses.KEY_DOWN and menu_actual.indice_actual < len(menu_actual.opciones) - 1:
                menu_actual.indice_actual += 1
            elif tecla == ord(' ') or tecla == curses.KEY_ENTER or tecla in [10, 13]:
                destino_seleccionado = menu_actual.opciones[menu_actual.indice_actual][1]
                
                if destino_seleccionado == "VOLVER":
                    if len(self.pila_menus) > 1:
                        self.pila_menus.pop()
                elif destino_seleccionado == "SALIR":
                    break
                elif isinstance(destino_seleccionado, Menu):
                    self.pila_menus.append(destino_seleccionado)
                elif callable(destino_seleccionado):
                    # Invocación segura de la función vinculada al dispositivo
                    destino_seleccionado(self)
            elif tecla in [curses.KEY_LEFT, ord('b'), curses.KEY_BACKSPACE]:
                if len(self.pila_menus) > 1:
                    self.pila_menus.pop()
            elif tecla in [ord('q'), ord('Q')]:
                break


def inicializar_menu_principal():
    """Declara la estructura inicial del menú raíz."""
    menu_principal = Menu("Menú de opciones")
    
    # Mapeo de opciones dinámicas inyectando la instancia de la app mediante Callbacks
    menu_principal.agregar_opcion("[1] Emparejar un dispositivo", lambda app: app.generar_menu_dispositivos("pair", escanear=True))
    menu_principal.agregar_opcion("[2] Conectarse a un dispositivo", lambda app: app.generar_menu_dispositivos("connect", escanear=False))
    menu_principal.agregar_opcion("[3] Eliminar un dispositivo", lambda app: app.generar_menu_dispositivos("remove", escanear=False))
    menu_principal.agregar_opcion("[4] Desconectar un dispositivo", lambda app: app.generar_menu_dispositivos("disconnect", escanear=False))
    menu_principal.agregar_opcion("[5] Lista de dispositivos emparejados", lambda app: app.mostrar_lista_emparejados())
    menu_principal.agregar_opcion("[0] Salir", "SALIR")
    
    return menu_principal

def main():
    # Comprobación básica de la presencia de bluetoothctl en el sistema operativo
    if not os.path.exists("/usr/bin/bluetoothctl") and subprocess.run(['which', 'bluetoothctl'], stdout=subprocess.PIPE).returncode != 0:
        print("Error: El ejecutable 'bluetoothctl' (bluez) no está instalado en este sistema Linux.")
        sys.exit(1)
        
    menu_raiz = inicializar_menu_principal()
    curses.wrapper(lambda stdscr: AplicacionTUI(stdscr, menu_raiz).ejecutar())

if __name__ == "__main__":
    main()