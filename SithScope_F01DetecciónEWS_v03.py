#===============================================================
#FUNCION 0 - DETECCIÓN DE EQUIPOS INDUSTRIALES Y DETECCIÓN DE EWS
#===============================================================
def detectar_equipos_indus():
    # Ejecutar el comando para obtener la IP de la interfaz eth0
    try:
        result = subprocess.run(
            "ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1", 
            shell=True, 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        ip_local = result.stdout.decode().strip()
        print(f"[INFO] IP local del equipo (eth0): {ip_local}")
    except subprocess.CalledProcessError as e:
        print(f"[X] Error al obtener la IP de la interfaz eth0: {e}")
        return

    # Obtener la red local (subred) a partir de la IP obtenida
    ip_parts = ip_local.split(".")
    red_local = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
    print(f"[INFO] Escaneando la red: {red_local}")

    # NMAP
    nm = nmap.PortScanner()

    try:
        print("[*] Iniciando escaneo de red (sin ping)...")
        # Realizar escaneo en la red local sin hacer ping (Modo sigilosoo)
        nm.scan(hosts=red_local, arguments="-p 502,4840 -sS --open -Pn")

        equipos_detectados = {}

        # Revisar los equipos y los puertos TCP para ver si hay puertos asociados a protocolos industriales
        for host in nm.all_hosts():
            print(f"\n[INFO] Equipo detectado: {host}")
            equipos_detectados[host] = []

            puertos_industriales = [502, 44818, 4840, 2455]
            for puerto in puertos_industriales:
                if nm[host].has_tcp(puerto):
                    nombre_protocolo = "Desconocido"
                    if puerto == 502:
                        nombre_protocolo = "Modbus TCP"
                    elif puerto == 44818:
                        nombre_protocolo = "Allen-Bradley (Ethernet/IP)"
                    elif puerto == 4840:
                        nombre_protocolo = "OPC UA"
                    equipos_detectados[host].append((puerto, nombre_protocolo))

        # Mostrar el resumen de los equipos encontrados
        print("\n=== Resumen de equipos detectados ===")
        for host, puertos in equipos_detectados.items():
            if puertos:
                print(f"\nEquipo: {host}")
                for puerto, protocolo in puertos:
                    print(f"  Puerto: {puerto}, Protocolo: {protocolo}")
            else:
                print(f"\nEquipo: {host} (sin puertos industriales detectados)")

    except Exception as e:
        print(f"[X] Error al realizar el escaneo: {e}")
