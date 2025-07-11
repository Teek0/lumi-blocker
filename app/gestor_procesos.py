import psutil # Librería para gestionar procesos en Python
import time
from app.config import cargar_configuracion

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

def escanear_y_cerrar_apps(apps_bloqueadas):
    """
    Detecta qué apps están activas y las cierra si coinciden.
    Retorna un diccionario con los resultados: {nombre_app: [pid, pid, ...]}
    """
    procesos_activos = obtener_procesos_activos()
    cerrados_por_app = {}
    for app in apps_bloqueadas:
        if app in procesos_activos:
            cerrados = cerrar_proceso(app)
            if cerrados:
                cerrados_por_app[app] = cerrados

    return cerrados_por_app

def ejecutar_con_duracion(funcion, args=(), duracion=10, intervalo=1):
    """
    Ejecuta una función repetidamente durante 'duracion' segundos, 
    cada 'intervalo' segundos.
    """
    tiempo_inicio = time.time()
    while time.time() - tiempo_inicio < duracion:
        funcion(*args)
        time.sleep(intervalo)

def bucle_bloqueo_procesos(duracion_segundos=10, intervalo=1):
    """
    Ejecuta un bucle de bloqueo durante cierto tiempo o hasta Ctrl+C.
    """
    config = cargar_configuracion()
    apps = config.get("apps_bloqueadas", [])

    def tarea():
        resultado = escanear_y_cerrar_apps(apps)
        for app, pids in resultado.items():
            print(f"{app} cerrado (PID: {', '.join(map(str, pids))})")
    
    try:
        ejecutar_con_duracion(tarea, duracion=duracion_segundos, intervalo=intervalo)
    except KeyboardInterrupt:
        print("Bloqueo detenido manualmente.")

if __name__ == "__main__":
    bucle_bloqueo_procesos(duracion_segundos=10)