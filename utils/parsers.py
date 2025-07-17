

def parsear_duracion(duracion: str | int | float) -> int:
    """
    Convierte una duración como '25m', '2h', '90s' o un número (minutos por defecto) en segundos.

    - '90s' → 90
    - '25m' → 1500
    - '2h' → 7200
    - 30   → 1800 (minutos por defecto si no tiene sufijo)
    """
    if isinstance(duracion, (int, float)):
        return int(duracion * 60)  # minutos por defecto

    duracion = duracion.strip().lower()

    try:
        if duracion.endswith("h"):
            return int(float(duracion[:-1]) * 3600)
        elif duracion.endswith("m"):
            return int(float(duracion[:-1]) * 60)
        elif duracion.endswith("s"):
            return int(float(duracion[:-1]))
        else:
            # Si no hay sufijo, asumimos minutos
            return int(float(duracion)) * 60
    except ValueError:
        raise ValueError(f"Formato de duración inválido: {duracion}")