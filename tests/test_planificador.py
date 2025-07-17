import pytest
from unittest import mock
from app.planificador import modo_temporizador

def test_modo_temporizador_ejecuta_funcion_variadas_veces():
    mock_func = mock.Mock()

    with mock.patch("time.time") as mock_time, \
         mock.patch("time.sleep") as mock_sleep:

        mock_time.side_effect = [0, 1, 2, 3, 4, 5]

        modo_temporizador(mock_func, duracion_segundos=5)

        assert mock_func.call_count == 4
        mock_sleep.assert_called_with(1)