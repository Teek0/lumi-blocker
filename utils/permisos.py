import ctypes
import sys
import os

def es_administrador() -> bool:
    """
    Verifica si el script se está ejecutando con privilegios de administrador (Windows).
    Retorna True si tiene permisos elevados, False en caso contrario.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def reiniciar_como_admin():
    """
    Si el script no tiene permisos de administrador, lo relanza con permisos elevados.
    Esto solo funciona en Windows.
    """
    if not es_administrador():
        script = sys.argv[0]
        params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable, 
            f'"{script}" {params}',
            None,
            1
        )
        sys.exit()