#===============================================================
#FUNCION 5 - ENVIAR DATOS CONFIDENCIALES Y VERIFICAR RECEPCIÓN
#===============================================================
def enviar_y_verificar_datos():
    global SLAVE_ID, SLAVE_IP, BUFFER_DATOS_REGISTROS

    if SLAVE_ID is None or SLAVE_IP is None:
        print("[!] Primero ejecuta la función 0 para detectar un Slave ID.")
        return
    if not BUFFER_DATOS_REGISTROS:
        print("[!] No hay datos cargados en BUFFER_DATOS_REGISTROS. Ejecuta primero la función 2.")
        return

    client = ModbusTcpClient(SLAVE_IP, port=PORT, timeout=0.5)
    if not client.connect():
        print(f"[X] No se pudo conectar a {SLAVE_IP}:{PORT}")
        return

    try:
        print("[*] Enviando datos a registros estáticos...")
        regs_sorted = sorted(BUFFER_DATOS_REGISTROS.keys())
        # Escribir registro a registros
        for reg in regs_sorted:
            addr0 = reg - 40001 
            val = BUFFER_DATOS_REGISTROS[reg]
            try:
                wr = client.write_register(addr0, val, slave=SLAVE_ID)
                if wr and not wr.isError():
                    print(f"  [+] Registro {reg} ← {val} (OK)")
                else:
                    print(f"  [!] Error al escribir en registro {reg}")
            except Exception as e:
                print(f"  [X] Fallo en {reg}: {e}")

        #Verificación
        print("\n[*] Verificando recepción de datos...")
        first = regs_sorted[0]
        last  = regs_sorted[-1]
        start = first - 40001
        length = (last - first) + 1

        resp = client.read_holding_registers(start, length, slave=SLAVE_ID)
        if resp and not resp.isError():
            block = resp.registers 
            leidos = []
            for reg in regs_sorted:
                idx = reg - first
                leidos.append(block[idx])

            ok = True
            for reg, recibido in zip(regs_sorted, leidos):
                enviado = BUFFER_DATOS_REGISTROS[reg]
                if enviado == recibido:
                    print(f"  [OK] Registro {reg}: {recibido} coincide con lo enviado")
                else:
                    print(f"  [!] Registro {reg}: enviado {enviado}, recibido {recibido} (NO COINCIDE)")
                    ok = False

            reconstruido = registers_to_string(leidos)
            print(f"\n[→] Cadena reconstruida (según endianness actual): «{reconstruido}»")

            if ok:
                print("\n[✔] Todos los valores enviados se verificaron correctamente.")
            else:
                print("\n[!] Algunos valores no coinciden con lo enviado. Revisa endianness o mapeo.")
        else:
            print("[!] Error al leer registros para verificación.")

    finally:
        client.close()