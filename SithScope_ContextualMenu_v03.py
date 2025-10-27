#EXFILTRACIÓN DE INFORMACIÓN CON PROTOCOLOS INDUSTRIALES
#HACKRTU
#HERRAMIENTA MODULAR (FASE INCIAL DEL PROYECTO)
#V.03
#===============================================================
#===============================================================

#!/usr/bin/env python3
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
import time
import nmap
import socket
import subprocess
import psutil
import platform
import os

#===============================================================
#DATOS BASE DEL SISTEMA OBJETIVO
#===============================================================
IP = "10.1.0.130"
PORT = 502

#===============================================================
#VARIABLES GLOBALES NECESARIAS
#===============================================================
SLAVE_IP = None
SLAVE_ID = None
LAST_SCAN = {"readable": set(), "writable": set()}
REGISTROS_ESTATICOS_BLOCK = []
REGISTROS_DINAMICOS_BLOCK = []
BUFFER_DATOS_REGISTROS = {}

#===============================================================
#MENÚ CONTEXTUAL
#===============================================================
def show_banner():
    print(r"""
  ____  _ _   _     ____                       
 / ___|(_) |_| |__ / ___|  ___ ___  _ __   ___ 
 \___ \| | __| '_ \\___ \ / __/ _ \| '_ \ / _ \
  ___) | | |_| | | |___) | (_| (_) | |_) |  __/
 |____/|_|\__|_| |_|____/ \___\___/| .__/ \___|
                                   |_|         
--------------------------------------------
    		By HackRTU
--------------------------------------------                                             

      Industrial Protocol Exfiltration Tool
      -------------------
      0 - Detectar todos los equipos en la red con caracter industrial
      1 - Detectar si es una estación de ingeniería industrial
      2 - Modbus ID Reading (Device Identification)
      3 - Detectar registros estáticos y dinámicos
      4 - Cargar Config.txt en registros estáticos (sin enviar)
      5 - Enviar datos confidenciales y verificar recepción
      9 - Salir
    """)

def ask_int(prompt, default=None, minv=None, maxv=None):
    s = input(f"{prompt} " + (f"[{default}] " if default is not None else ""))
    if s.strip() == "" and default is not None:
        return default
    try:
        v = int(s)
    except ValueError:
        print("  → Valor no válido, intenta de nuevo.")
        return ask_int(prompt, default, minv, maxv)
    if minv is not None and v < minv:
        print(f"  → Debe ser >= {minv}")
        return ask_int(prompt, default, minv, maxv)
    if maxv is not None and v > maxv:
        print(f"  → Debe ser <= {maxv}")
        return ask_int(prompt, default, minv, maxv)
    return v

def ask_float(prompt, default=None, minv=None, maxv=None):
    s = input(f"{prompt} " + (f"[{default}] " if default is not None else ""))
    if s.strip() == "" and default is not None:
        return default
    try:
        v = float(s)
    except ValueError:
        print("  → Valor no válido, intenta de nuevo.")
        return ask_float(prompt, default, minv, maxv)
    if minv is not None and v < minv:
        print(f"  → Debe ser >= {minv}")
        return ask_float(prompt, default, minv, maxv)
    if maxv is not None and v > maxv:
        print(f"  → Debe ser <= {maxv}")
        return ask_float(prompt, default, minv, maxv)
    return v

def ask_yesno(prompt, default="n"):
    s = input(f"{prompt} [{'Y' if default.lower()=='y' else 'y'}/{'N' if default.lower()=='n' else 'n'}] ").strip().lower()
    if s == "":
        s = default.lower()
    return s.startswith("y")
    
#===============================================================
# BLUCLE PRINCIPAL
#===============================================================
def main():
    while True:
        show_banner()
        opcion = ask_int("Elige opción:", minv=0, maxv=9)
        if opcion == 0:
            detectar_equipos_indus()  # Detección de equipos industriales
        elif opcion == 1:
            detectar_estacion_ingenieria()  # Detección de estación de ingeniería
        elif opcion == 2:
            scan_slave_ids()  # Detectar Modbus Slave ID
        elif opcion == 3:
            detect_holding_registers()  # Detectar registros estáticos/dinámicos
        elif opcion == 4:
            cargar_config_en_registros()  # Cargar Config.txt
        elif opcion == 5:
            enviar_y_verificar_datos()  # Enviar y verificar datos
        elif opcion == 9:
            print("Saliendo...")
            break
        else:
            print("[!] Opción no válida.")

if __name__ == "__main__":
    main()         
    