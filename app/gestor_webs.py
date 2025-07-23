import os # Sirve para manejar rutas de archivos
import platform # Para detectar el sistema operativo
import subprocess # Para ejecutar comandos del sistema
from app.logger_bloqueo import registrar_evento_bloqueo

RUTA_HOSTS = r"C:\Windows\System32\drivers\etc\hosts" if platform.system() == "Windows" else "/etc/hosts"
MARCA_INICIO = "# === BLOQUEO LUMIBLOCKER INICIO ===\n"
MARCA_FIN = "# === BLOQUEO LUMIBLOCKER FIN ===\n"

def bloquear_webs(dominios):
    """
    Agrega líneas al archivo hosts para bloquear los dominios dados.
    """
    if not isinstance(dominios, list) or not dominios:
        raise ValueError("Se requiere una lista de dominios para bloquear.")
    try:
        with open(RUTA_HOSTS, "r", encoding="utf-8") as f:
            contenido = f.readlines()
    except PermissionError:
        registrar_evento_bloqueo("error", "bloquear_webs", None, "PermissionError al leer hosts")
        print("No tienes permisos suficientes para modificar el archivo hosts.")
        return


# Eliminar secciones antiguas si existen
    nuevo_contenido = []
    dentro_de_bloque = False
    for linea in contenido:
        if linea == MARCA_INICIO:
            dentro_de_bloque = True
            continue
        elif linea == MARCA_FIN:
            dentro_de_bloque = False
            continue
        if not dentro_de_bloque:
            nuevo_contenido.append(linea)

    # Agregar los nuevos bloqueos
    bloque = [MARCA_INICIO]
    for dominio in dominios:
        bloque.append(f"127.0.0.1 {dominio}\n")
        bloque.append(f"::1 {dominio}\n")  # IPv6
        registrar_evento_bloqueo("web", dominio, None, "bloqueado")
    bloque.append(MARCA_FIN)

    nuevo_contenido.extend(bloque)

    try:
        with open(RUTA_HOSTS, "w", encoding="utf-8") as f:
            f.writelines(nuevo_contenido)
        print("Sitios bloqueados correctamente.")
    except PermissionError:
        print("No se pudo escribir en el archivo hosts. Ejecuta como administrador.")


def restaurar_hosts_original():
    """
    Elimina la sección de bloqueo agregada por LumiBlocker en el archivo hosts.
    """
    try:
        with open(RUTA_HOSTS, "r", encoding="utf-8") as f:
            contenido = f.readlines()
    except PermissionError:
        registrar_evento_bloqueo("error", "restaurar_hosts_original", None, "PermissionError al leer hosts")
        print("No tienes permisos suficientes para modificar el archivo hosts.")
        return

    nuevo_contenido = []
    dentro_de_bloque = False
    for linea in contenido:
        if linea == MARCA_INICIO:
            dentro_de_bloque = True
            continue
        elif linea == MARCA_FIN:
            dentro_de_bloque = False
            continue
        if not dentro_de_bloque:
            nuevo_contenido.append(linea)

    try:
        with open(RUTA_HOSTS, "w", encoding="utf-8") as f:
            f.writelines(nuevo_contenido)
        print("Bloqueo de sitios web desactivado.")
        registrar_evento_bloqueo("web", "todos", None, "restaurado")
    except PermissionError:
        print("No se pudo escribir en el archivo hosts. Ejecuta como administrador.")


def flush_dns():
    """
    Limpia la caché DNS del sistema operativo para que surtan efecto los cambios en hosts.
    Solo tiene efecto en sistemas compatibles (Windows, Linux con systemd-resolved, etc.).
    """
    sistema = platform.system()

    try:
        if sistema == "Windows":
            subprocess.run(["ipconfig", "/flushdns"], check=True)
        elif sistema == "Linux":
            subprocess.run(["systemd-resolve", "--flush-caches"], check=True)
        elif sistema == "Darwin":
            subprocess.run(["dscacheutil", "-flushcache"], check=True)
            subprocess.run(["killall", "-HUP", "mDNSResponder"], check=True)
        else:
            print(f"No se reconoce el sistema operativo: {sistema}")
            return

        print("Caché DNS vaciada correctamente.")
    except Exception as e:
        print(f"No se pudo limpiar la caché DNS: {e}")