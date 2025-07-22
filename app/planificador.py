import time
import json
from datetime import datetime
import os

ESTADO_PATH = "estado_bloqueo.json"

def modo_temporizador(func, duracion_segundos: int, *args, **kwargs):
    """
    Ejecuta la función `func` durante X segundos, luego la detiene.
    """
    inicio = time.time()
    while time.time() - inicio < duracion_segundos:
        func(*args, **kwargs)
        time.sleep(1)

# Función auxiliar para test
def _modo_horario_iter(func, hora_inicio: str, hora_fin: str, intervalo: int = 60, *args, **kwargs):
    """
    Versión iterativa para testeo de modo_horario. Lanza StopIteration tras una sola vuelta.
    """
    h_inicio = datetime.strptime(hora_inicio, "%H:%M").time()
    h_fin = datetime.strptime(hora_fin, "%H:%M").time()

    ahora = datetime.now().time()
    en_rango = h_inicio <= ahora < h_fin if h_inicio < h_fin else (ahora >= h_inicio or ahora < h_fin)

    if en_rango:
        func(*args, **kwargs)

    raise StopIteration  # cortar para test

def modo_horario(func, hora_inicio, hora_fin, intervalo=60, *args, **kwargs):
    """
    Ejecuta la función `func` solo cuando la hora actual esté dentro del rango [hora_inicio, hora_fin).
    
    - hora_inicio y hora_fin son strings en formato "HH:MM"
    - intervalo es el tiempo en segundos entre verificaciones
    - La función se repite indefinidamente mientras esté dentro del horario
    """
    # Paso 1: Convertir strings a objetos datetime.time
    h_inicio = datetime.strptime(hora_inicio, "%H:%M").time()
    h_fin = datetime.strptime(hora_fin, "%H:%M").time()

    print(f"Esperando bloque horario: {h_inicio} - {h_fin}")

    while True:
        ahora = datetime.now().time()

        # Validación de rango de hora
        en_rango = h_inicio <= ahora < h_fin if h_inicio < h_fin else (ahora >= h_inicio or ahora < h_fin)

        if en_rango:
            print(f"[{ahora.strftime('%H:%M:%S')}] Dentro del horario. Ejecutando función.")
            func(*args, **kwargs)
        else:
            print(f"[{ahora.strftime('%H:%M:%S')}] Fuera del horario. Esperando...")

        time.sleep(intervalo)

def modo_permanente(func, intervalo: int = 60, *args, **kwargs):
    """
    Ejecuta la función `func` indefinidamente mientras `permanente_activado` sea True
    en el archivo estado_bloqueo.json. Sirve como modo ON/OFF general.
    """
    print("Bloqueo permanente activado. Esperando señal para desactivar...")

    while True:
        if not estado_permanente_activado():
            print("Bloqueo permanente desactivado.")
            break

        func(*args, **kwargs)
        time.sleep(intervalo)


def estado_permanente_activado() -> bool:
    """
    Devuelve True si el archivo JSON de estado indica que el modo permanente está activo.
    Si no existe o hay error de lectura, devuelve False.
    """
    if not os.path.exists(ESTADO_PATH):
        return False

    try:
        with open(ESTADO_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("permanente_activado", False)
    except Exception:
        return False