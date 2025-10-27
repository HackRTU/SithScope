#===============================================================
#FUNCION 4 - LEER CONFIG.TXT Y MAPEAR A LOS REGISTROS ESTÁTICOS
#===============================================================
def cargar_config_en_registros():
    global REGISTROS_ESTATICOS_BLOCK, BUFFER_DATOS_REGISTROS

    if not REGISTROS_ESTATICOS_BLOCK:
        print("[!] No hay registros estáticos detectados. Ejecuta primero la función 1.")
        return

    ruta_config = "/home/hackrtu/00_HACKRTU/00_INVESTIGACIONES/Config.txt"

    try:
        with open(ruta_config, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
    except Exception as e:
        print(f"[X] Error al leer {ruta_config}: {e}")
        return

    # Ordenar los registros estáticos en ascendente para garantizar alineación
    regs_sorted = sorted(REGISTROS_ESTATICOS_BLOCK)
    max_regs = len(regs_sorted)

    # Empaquetar string -> registros 16-bit con el esquema de endianness elegido
    valores = string_to_registers(contenido, max_registers=max_regs)

    # Relleno si faltan registros (con 0x0000)
    if len(valores) < max_regs:
        valores += [0] * (max_regs - len(valores))

    # Guardar mapeo (registro -> valor) manteniendo el orden
    BUFFER_DATOS_REGISTROS = {reg: val for reg, val in zip(regs_sorted, valores)}

    print("[OK] Config.txt cargado y mapeado a registros estáticos (sin enviar).")
    for reg in regs_sorted:
        print(f"  Registro {reg} ← {BUFFER_DATOS_REGISTROS[reg]}")