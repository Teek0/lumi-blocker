import pytest
import sys
from unittest import mock
from utils import permisos

def test_es_administrador_true():
    with mock.patch("ctypes.windll.shell32.IsUserAnAdmin", return_value=True):
        assert permisos.es_administrador() is True

def test_es_administrador_false():
    with mock.patch("ctypes.windll.shell32.IsUserAnAdmin", return_value=False):
        assert permisos.es_administrador() is False

def test_es_administrador_exception():
    with mock.patch("ctypes.windll.shell32.IsUserAnAdmin", side_effect=Exception("fallo")):
        assert permisos.es_administrador() is False

def test_reiniciar_como_admin_lanza_script_si_no_es_admin():
    with mock.patch("utils.permisos.es_administrador", return_value=False), \
         mock.patch("ctypes.windll.shell32.ShellExecuteW") as mock_shell, \
         mock.patch("sys.exit") as mock_exit, \
         mock.patch("sys.argv", ["main.py", "block", "websites"]), \
         mock.patch("sys.executable", "python"):

        permisos.reiniciar_como_admin()

        mock_shell.assert_called_once()
        mock_exit.assert_called_once()

def test_reiniciar_como_admin_no_hace_nada_si_es_admin():
    with mock.patch("utils.permisos.es_administrador", return_value=True), \
         mock.patch("ctypes.windll.shell32.ShellExecuteW") as mock_shell, \
         mock.patch("sys.exit") as mock_exit:

        permisos.reiniciar_como_admin()

        mock_shell.assert_not_called()
        mock_exit.assert_not_called()
