from unittest import mock
from app.planificador import _modo_horario_iter, modo_temporizador
import datetime
import pytest

def test_modo_temporizador_ejecuta_funcion_variadas_veces():
    mock_func = mock.Mock()

    with mock.patch("time.time") as mock_time, \
         mock.patch("time.sleep") as mock_sleep:

        mock_time.side_effect = [0, 1, 2, 3, 4, 5]

        modo_temporizador(mock_func, duracion_segundos=5)

        assert mock_func.call_count == 4
        mock_sleep.assert_called_with(1)


def test_modo_horario_ejecuta_funcion_en_rango():
    mock_func = mock.Mock()

    hora_simulada = datetime.time(10, 0)

    with mock.patch("app.planificador.datetime") as mock_datetime, \
         mock.patch("time.sleep"), \
         mock.patch("builtins.print"):

        mock_datetime.now.return_value = datetime.datetime.combine(
            datetime.date.today(), hora_simulada
        )

        # PERO ahora forzamos que datetime.strptime siga funcionando
        mock_datetime.strptime = datetime.datetime.strptime

        with pytest.raises(StopIteration):
            next(_modo_horario_iter(mock_func, "09:00", "11:00"))

    mock_func.assert_called_once()


def test_modo_horario_no_ejecuta_fuera_de_rango():
    mock_func = mock.Mock()

    hora_simulada = datetime.time(14, 0)

    with mock.patch("app.planificador.datetime") as mock_datetime, \
         mock.patch("time.sleep"), \
         mock.patch("builtins.print"):

        mock_datetime.now.return_value = datetime.datetime.combine(
            datetime.date.today(), hora_simulada
        )

        mock_datetime.strptime = datetime.datetime.strptime

        with pytest.raises(StopIteration):
            next(_modo_horario_iter(mock_func, "09:00", "11:00"))

    mock_func.assert_not_called()
