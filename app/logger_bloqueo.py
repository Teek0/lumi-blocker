import json
import os
from datetime import datetime
from pathlib import Path

RUTA_LOGS = Path("logs.json")


def registrar_evento_bloqueo(tipo: str, nombre: str, pid: int | None, resultado: str):
    """
    Registra un evento de intento de bloqueo en logs.json.

    Args:
        tipo: 'app' o 'web'
        nombre: Nombre del proceso o dominio bloqueado
        pid: PID del proceso (si aplica), None para webs
        resultado: 'cerrado', 'protegido', 'no encontrado', 'error', etc.
    """
    evento = {
        "timestamp": datetime.now().isoformat(),
        "tipo": tipo,
        "nombre": nombre,
        "pid": pid,
        "resultado": resultado,
    }

    logs = []
    
    # Si el archivo ya existe, lo cargamos
    if RUTA_LOGS.exists():
        try:
            with open(RUTA_LOGS, "r", encoding="utf-8") as f:
                contenido = json.load(f)
                if isinstance(contenido, list):
                    logs = contenido
        except json.JSONDecodeError:
            logs = []  # archivo corrupto → reiniciamos

    logs.append(evento)

    with open(RUTA_LOGS, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)
