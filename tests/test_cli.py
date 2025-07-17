from typer.testing import CliRunner
from main import app
from unittest.mock import patch
import shutil
import os

runner = CliRunner()

def test_comando_block_apps_con_args():
    with patch("main.bucle_bloqueo_procesos") as mock_bucle:
        result = runner.invoke(app, ["block", "apps", "--duracion", "2", "--intervalo", "1"])

        assert result.exit_code == 0
        assert "Bloqueando apps por 2.0 segundos" in result.output
        mock_bucle.assert_called_once_with(duracion_segundos=2.0, intervalo=1.0)

def test_block_websites_con_config_real():
    os.environ["TESTING"] = "1"  # evita ejecutar reiniciar_como_admin()

    result = runner.invoke(app, [
        "block", "websites",
        "--config-path", "tests/data/config_test.json"
    ])

    print("OUTPUT:", result.output)
    assert result.exit_code == 0
    assert "youtube.com" in result.output
    assert "Sitios bloqueados." in result.output

def test_unblock_websites_output():
    os.environ["TESTING"] = "1"  # evita ejecutar reiniciar_como_admin()
    
    result = runner.invoke(app, ["unblock", "websites"])

    print("OUTPUT:", result.output)
    assert result.exit_code == 0
    assert "Sitios desbloqueados correctamente." in result.output

