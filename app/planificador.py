import time
from datetime import datetime

def modo_temporizador(func, duracion_segundos: int, *args, **kwargs):
    """
    Ejecuta la función `func` durante X segundos, luego la detiene.
    """
    inicio = time.time()
    while time.time() - inicio < duracion_segundos:
        func(*args, **kwargs)
        time.sleep(1)
