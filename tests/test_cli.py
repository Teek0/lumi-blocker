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

def test_cli_block_websites():
    config_falsa = {
        "webs_bloqueadas": ["youtube.com", "facebook.com"]
    }

    with patch("main.cargar_configuracion", return_value=config_falsa):
        with patch("main.bloquear_webs") as mock_bloquear:
            with patch("main.flush_dns") as mock_flush:
                result = runner.invoke(app, ["block", "websites"])

                assert result.exit_code == 0
                assert "youtube.com" in result.stdout
                assert "facebook.com" in result.stdout
                mock_bloquear.assert_called_once_with(["youtube.com", "facebook.com"])
                mock_flush.assert_called_once()

def test_cli_unblock_websites():
    with patch("main.restaurar_hosts_original") as mock_restaurar:
        with patch("main.flush_dns") as mock_flush:
            result = runner.invoke(app, ["unblock", "websites"])

            assert result.exit_code == 0
            assert "Sitios desbloqueados correctamente." in result.stdout
            mock_restaurar.assert_called_once()
            mock_flush.assert_called_once()