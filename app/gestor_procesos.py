import psutil # Librería para gestionar procesos en Python

def obtener_procesos_activos():
    """
    Retorna una lista de nombres de procesos actualmente en ejecución.
    """
    nombres = []
    for proc in psutil.process_iter(['name']):
        try:
            nombres.append(proc.info['name'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return nombres

def cerrar_proceso(nombre_objetivo):
    """
    Intenta cerrar todos los procesos cuyo nombre coincida con el nombre_objetivo.
    Retorna una lista con los PID de los procesos cerrados.
    """
    cerrados = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] == nombre_objetivo:
                proc.terminate()
                cerrados.append(proc.info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return cerrados
