from app.gestor_webs import bloquear_webs, MARCA_INICIO, MARCA_FIN, restaurar_hosts_original, flush_dns
from unittest.mock import patch, mock_open
from unittest import mock
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

def test_bloquear_webs_registra_logs():
    dominios = ["facebook.com", "twitter.com"]
    contenido_hosts = [
        "127.0.0.1 localhost\n",
        "# === BLOQUEO LUMIBLOCKER INICIO ===\n",
        "127.0.0.1 oldsite.com\n",
        "# === BLOQUEO LUMIBLOCKER FIN ===\n",
    ]

    m = mock_open(read_data="".join(contenido_hosts))

    with patch("app.gestor_webs.open", m):
        with patch("app.gestor_webs.registrar_evento_bloqueo") as mock_log:
            bloquear_webs(dominios)
            for dominio in dominios:
                mock_log.assert_any_call("web", dominio, None, "bloqueado")

def test_restaurar_hosts_registra_log():
    contenido_hosts = [
        "127.0.0.1 localhost\n",
        "# === BLOQUEO LUMIBLOCKER INICIO ===\n",
        "127.0.0.1 facebook.com\n",
        "# === BLOQUEO LUMIBLOCKER FIN ===\n",
        "192.168.1.1 router.local\n",
    ]

    m = mock_open(read_data="".join(contenido_hosts))

    with patch("app.gestor_webs.open", m):
        with patch("app.gestor_webs.registrar_evento_bloqueo") as mock_log:
            restaurar_hosts_original()
            mock_log.assert_called_with("web", "todos", None, "restaurado")

def test_bloquear_webs_loguea_error_si_falla_lectura():
    dominios = ["bloqueame.com"]

    with patch("app.gestor_webs.open", side_effect=PermissionError("sin permiso")), \
         patch("app.gestor_webs.registrar_evento_bloqueo") as mock_log:

        bloquear_webs(dominios)

        mock_log.assert_any_call("error", "bloquear_webs", None, "PermissionError al leer hosts")

