from typer.testing import CliRunner
from main import app
from unittest.mock import patch
import shutil
import os

runner = CliRunner()

def test_comando_block_apps_modo_temporizador():
    with patch("main.bucle_bloqueo_procesos") as mock_bucle, \
         patch("main.modo_temporizador") as mock_temporizador:
        result = runner.invoke(app, [
            "block", "apps",
            "--modo", "temporizador",
            "--duracion", "2m",
            "--intervalo", "1"
        ])

        assert result.exit_code == 0
        mock_temporizador.assert_called_once()
        mock_bucle.assert_not_called()  # la lógica está en el wrapper que pasa a temporizador

def test_block_websites_modo_temporizador():
    os.environ["TESTING"] = "1"  # evita ejecutar reiniciar_como_admin()

    with patch("app.gestor_webs.bloquear_webs") as mock_bloquear_webs, \
         patch("app.gestor_webs.flush_dns") as mock_flush, \
         patch("main.modo_temporizador") as mock_temporizador:

        result = runner.invoke(app, [
            "block", "websites",
            "--modo", "temporizador",
            "--duracion", "1m",
            "--config-path", "tests/data/config_test.json"
        ])

        assert result.exit_code == 0
        mock_temporizador.assert_called_once()
        mock_bloquear_webs.assert_not_called()  # se llama dentro de temporizador
        mock_flush.assert_not_called()

def test_unblock_websites_output():
    os.environ["TESTING"] = "1"  # evita ejecutar reiniciar_como_admin()

    with patch("main.restaurar_hosts_original") as mock_restaurar, \
         patch("main.flush_dns") as mock_flush:
        
        result = runner.invoke(app, ["unblock", "websites"])

        assert result.exit_code == 0
        assert "Sitios desbloqueados correctamente." in result.output
        mock_restaurar.assert_called_once()
        mock_flush.assert_called_once()

