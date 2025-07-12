from typer.testing import CliRunner
from main import app
from unittest.mock import patch

runner = CliRunner()

def test_comando_block_apps_con_args():
    with patch("main.bucle_bloqueo_procesos") as mock_bucle:
        result = runner.invoke(app, ["block", "apps", "--duracion", "2", "--intervalo", "1"])

        assert result.exit_code == 0
        assert "Bloqueando apps por 2.0 segundos" in result.stdout
        mock_bucle.assert_called_once_with(duracion_segundos=2.0, intervalo=1.0)
