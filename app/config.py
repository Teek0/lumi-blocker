import json

def cargar_configuracion(ruta="config.json"):
    """
    Carga el archivo de configuración y returna un diccionario
    """
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)