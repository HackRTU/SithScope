#===============================================================
#FUNCION 3 - DETECTAR REGISTROS ESTÁTICOS Y DINÁMICOS
#Revisión de los registros sobre los que podría llegar a escribirse para la exfiltración de la información.
#===============================================================
def detect_holding_registers():
    global SLAVE_ID, SLAVE_IP, REGISTROS_ESTATICOS_BLOCK, REGISTROS_DINAMICOS_BLOCK
    REGISTROS_ESTATICOS_BLOCK = []
    REGISTROS_DINAMICOS_BLOCK = []

    if SLAVE_ID is None:
        print("[!] Primero ejecuta la función 0 para detectar un Slave ID.")
        return

    start_modbus = 40221 #Pruebas específicas, con SithScope versión final se revisarán todos los registros.
    end_modbus   = 40240
    consecutive_needed = 10 #Valor genérico para pruebas iniciales.

    client = ModbusTcpClient(SLAVE_IP, port=PORT, timeout=0.5)
    if not client.connect():
        print(f"[X] No se pudo conectar a {SLAVE_IP}:{PORT}")
        return

    consecutive = []
    current = start_modbus

    try:
        while current <= end_modbus and len(consecutive) < consecutive_needed:
            addr = current - 40001  # convertir a base 0

            try:
                resp1 = client.read_holding_registers(addr, 1, slave=SLAVE_ID)
                if resp1 is None or resp1.isError():
                    print(f"  [!] Registro {current} no disponible.")
                    consecutive.clear()
                    current += 1
                    continue
                val1 = resp1.registers[0]

                time.sleep(1)

                resp2 = client.read_holding_registers(addr, 1, slave=SLAVE_ID)
                if resp2 is None or resp2.isError():
                    print(f"  [!] Registro {current} no disponible en segunda lectura.")
                    consecutive.clear()
                    current += 1
                    continue
                val2 = resp2.registers[0]

                if val1 == val2:
                    print(f"  [+] Registro {current} es ESTÁTICO (valor {val1})")
                    consecutive.append(current)
                else:
                    print(f"  [!] Registro {current} cambió entre lecturas ({val1} → {val2})")
                    REGISTROS_DINAMICOS_BLOCK.append(current)
                    consecutive.clear()

            except Exception as e:
                print(f"  [X] Error leyendo {current}: {e}")
                consecutive.clear()

            current += 1

        if len(consecutive) >= consecutive_needed:
            REGISTROS_ESTATICOS_BLOCK = consecutive.copy()
            print(f"\n[OK] Encontrados {consecutive_needed} registros consecutivos estáticos: {REGISTROS_ESTATICOS_BLOCK}")
        else:
            print(f"\n[!] No se encontraron {consecutive_needed} registros estáticos consecutivos en el rango {start_modbus}-{end_modbus}")

        LAST_SCAN["readable"].update(REGISTROS_ESTATICOS_BLOCK + REGISTROS_DINAMICOS_BLOCK)

    finally:
        client.close()