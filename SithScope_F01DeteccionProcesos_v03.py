#===============================================================
#FUNCION 1 - Detección de Estación de Ingeniería (EWS)
#Diferentes procesos que suelen encontrarse en estaciones de ingeniería.
#===============================================================
def detectar_estacion_ingenieria():
    sospechas = []

    so = platform.system()
    print(f"[*] Sistema operativo detectado: {so}")
    if so != "Windows":
        print("[!] Advertencia: la mayoría de estaciones de ingeniería usan Windows. Resultados limitados.\n")

    procesos_objetivo = {
        "Siemens TIA Portal": ["Siemens.Automation.Portal", "S7oiehsx64x"],
        "Siemens Step7/PCS7": ["s7oiehsx.exe"],
        "Siemens WinCC": ["CCProjectMgr", "WinCCRuntime"],
        "Codesys": ["CODESYS.exe", "codesyscontrol"],
        "Rockwell Studio5000": ["RSLogix5000.exe"],
        "Schneider EcoStruxure/Unity": ["UnityXL.exe"],
        "Beckhoff TwinCAT": ["TcSysSrv.exe"],
        "Mitsubishi GX Works": ["GXWorks2.exe"]
    }

    procesos_actuales = [p.name() for p in psutil.process_iter(attrs=['name'])]
    for herramienta, nombres in procesos_objetivo.items():
        for proc in nombres:
            if any(proc.lower() in p.lower() for p in procesos_actuales):
                sospechas.append(f"{herramienta} (proceso {proc})")
                
    #Rutas comunes en las que suele encontrarse el software de ingeniería dentro de una EWS.
    rutas_comunes = {
        "Siemens": [
            "C:\\Program Files\\Siemens\\Automation",
            "C:\\Program Files (x86)\\Siemens\\Automation"
        ],
        "Codesys": ["C:\\Program Files\\3S Software\\CODESYS"],
        "Rockwell": ["C:\\Program Files\\Rockwell Software"],
        "Schneider": ["C:\\Program Files (x86)\\Schneider Electric"],
        "Beckhoff": ["C:\\TwinCAT"],
        "Mitsubishi": ["C:\\Program Files (x86)\\MELSOFT"]
    }

    for herramienta, paths in rutas_comunes.items():
        for ruta in paths:
            if os.path.exists(ruta):
                sospechas.append(f"{herramienta} (directorio {ruta})")

    print("\n=== RESULTADO DETECCIÓN EWS ===")
    if sospechas:
        print("[OK] La máquina presenta indicios de ser una Estación de Ingeniería:")
        for s in sospechas:
            print(f"   - {s}")
    else:
        print("[!] No se detectaron herramientas típicas de ingeniería en este host.")ó