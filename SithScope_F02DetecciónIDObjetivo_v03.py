#===============================================================
#FUNCION 2 - FUNCIÓN PARA DETECTAR EL ID DEL OBJETIVO
#Detección por Modbus del ID del objetivo.
#===============================================================
def scan_slave_ids():
    global SLAVE_ID, SLAVE_IP
    client = ModbusTcpClient(IP, port=PORT, timeout=0.5)
    if client.connect():
        try:
            for uid in range(1, 248):   # escaneo básico
                rr = client.read_device_information(slave=uid)
                if rr is not None and not rr.isError():
                    SLAVE_ID = uid
                    SLAVE_IP = IP
                    break
        except Exception:
            pass
        finally:
            client.close()

        if SLAVE_ID is not None:
            print(f"[OK] Encontrado slave ID: {SLAVE_ID}")
        else:
            print("[!] Ningún slave ID respondió.")
    else:
        print(f"[X] No se pudo conectar a {IP}:{PORT}")