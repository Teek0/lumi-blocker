import json

def cargar_configuracion(ruta: str = "config.json"):
    """
    Carga el archivo de configuración y returna un diccionario
    """
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}