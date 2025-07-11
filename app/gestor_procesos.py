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

def bucle_bloqueo_procesos(duracion_segundos=10, intervalo=1):
    """
    Ejecuta un bucle que durante 'duracion_seugndos' segundos busca y cierra procesos bloqueados.
    También puede detenerse antes con Ctrl+C.
    """
    config = cargar_configuracion()
    apps_bloqueadas = config.get("apps_bloqueadas", [])

    print(f"Iniciando bloqueo durante {duracion_segundos} segundos. Ctrl+C para detener.")

    tiempo_inicio = time.time()

    try:
        while True:
            tiempo_actual = time.time()
            if tiempo_actual - tiempo_inicio > duracion_segundos:
                print("Duración alcanzada. Finalizando bloqueo.")
                break
            procesos_activos = obtener_procesos_activos()
            for app in apps_bloqueadas:
                if app in procesos_activos:
                    cerrados = cerrar_proceso(app)
                    if cerrados:
                        print(f"Proceso cerrado: {app} (PID: {', '.join(map(str, cerrados))})")
            time.sleep(intervalo)
    except KeyboardInterrupt:
        print("Bucle de bloqueo interrumpido por el usuario.")


if __name__ == "__main__":
    bucle_bloqueo_procesos(duracion_segundos=10)