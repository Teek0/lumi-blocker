from app.gestor_webs import bloquear_webs, MARCA_INICIO, MARCA_FIN, restaurar_hosts_original, flush_dns
from unittest.mock import patch, mock_open
import platform

def test_bloquear_webs_agrega_dominios():
    dominios = ["youtube.com", "twitter.com"]
    contenido_original = ["127.0.0.1 localhost\n", "# Otro comentario\n"]

    m = mock_open(read_data="".join(contenido_original))

    with patch("app.gestor_webs.open", m):
        bloquear_webs(dominios)

    handle = m()
    handle.write.assert_not_called()

    bloque_esperado = [
        MARCA_INICIO,
        "127.0.0.1 youtube.com\n",
        "::1 youtube.com\n",
        "127.0.0.1 twitter.com\n",
        "::1 twitter.com\n",
        MARCA_FIN
    ]
    contenido_escrito = "".join(contenido_original) + "".join(bloque_esperado)
    m().writelines.assert_called_once()
    m().writelines.assert_called_once_with(contenido_original + bloque_esperado)

def test_restaurar_hosts_elimina_bloque():
    contenido_con_bloque = [
        "127.0.0.1 localhost\n",
        "# Otro comentario\n",
        "# === BLOQUEO LUMIBLOCKER INICIO ===\n",
        "127.0.0.1 youtube.com\n",
        "::1 youtube.com\n",
        "# === BLOQUEO LUMIBLOCKER FIN ===\n",
        "192.168.0.1 router\n"
    ]

    m = mock_open(read_data="".join(contenido_con_bloque))

    with patch("app.gestor_webs.open", m):
        restaurar_hosts_original()

    handle = m()
    m().writelines.assert_called_once_with([
        "127.0.0.1 localhost\n",
        "# Otro comentario\n",
        "192.168.0.1 router\n"
    ])

@patch("app.gestor_webs.subprocess.run")
def test_flush_dns_windows(mock_run):
    with patch("app.gestor_webs.platform.system", return_value="Windows"):
        flush_dns()
        mock_run.assert_called_once_with(["ipconfig", "/flushdns"], check=True)