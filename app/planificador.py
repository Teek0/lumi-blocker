import time
import json
from datetime import datetime
import os
from app.logger_bloqueo import registrar_evento_bloqueo

ESTADO_PATH = "estado_bloqueo.json"

def modo_temporizador(func, duracion_segundos: int, *args, **kwargs):
    """
    Ejecuta la función `func` durante X segundos, luego la detiene.
    Registra el inicio y final o interrupción en logs.json.
    """
    nombre = kwargs.get("nombre", "desconocido")
    registrar_evento_bloqueo("sesion", nombre, None, f"iniciada (modo: temporizador, duración: {duracion_segundos}s)")

    inicio = time.time()
    try:
        while time.time() - inicio < duracion_segundos:
            func(*args, **kwargs)
            time.sleep(1)
    except KeyboardInterrupt:
        registrar_evento_bloqueo("sesion", nombre, None, "detenida manualmente")
        print("Sesión interrumpida manualmente.")
    else:
        registrar_evento_bloqueo("sesion", nombre, None, "finalizada")


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
    Registra la sesión completa (inicio, y fin si es interrumpida).
    """
    h_inicio = datetime.strptime(hora_inicio, "%H:%M").time()
    h_fin = datetime.strptime(hora_fin, "%H:%M").time()
    nombre = kwargs.get("nombre", "desconocido")

    registrar_evento_bloqueo("sesion", nombre, None, f"iniciada (modo: horario, rango: {hora_inicio} - {hora_fin})")
    print(f"Esperando bloque horario: {h_inicio} - {h_fin}")

    try:
        while True:
            ahora = datetime.now().time()

            en_rango = h_inicio <= ahora < h_fin if h_inicio < h_fin else (ahora >= h_inicio or ahora < h_fin)

            if en_rango:
                print(f"[{ahora.strftime('%H:%M:%S')}] Dentro del horario. Ejecutando función.")
                func(*args, **kwargs)
            else:
                print(f"[{ahora.strftime('%H:%M:%S')}] Fuera del horario. Esperando...")

            time.sleep(intervalo)
    except KeyboardInterrupt:
        registrar_evento_bloqueo("sesion", nombre, None, "detenida manualmente")
        print("Sesión interrumpida manualmente.")


def modo_permanente(func, intervalo: int = 60, *args, **kwargs):
    """
    Ejecuta la función `func` indefinidamente mientras `permanente_activado` sea True
    en el archivo estado_bloqueo.json. Sirve como modo ON/OFF general.
    """
    nombre = kwargs.get("nombre", "desconocido")
    registrar_evento_bloqueo("sesion", nombre, None, "iniciada (modo: permanente)")
    print("Bloqueo permanente activado. Esperando señal para desactivar...")

    while True:
        if not estado_permanente_activado():
            registrar_evento_bloqueo("sesion", nombre, None, "finalizada")
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
    except Exception as e:
        registrar_evento_bloqueo("error", "estado_permanente_activado", None, f"error: {type(e).__name__}")
        return False