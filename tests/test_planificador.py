from unittest import mock
from app.planificador import _modo_horario_iter, modo_temporizador, modo_permanente, estado_permanente_activado
import builtins
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


def test_estado_permanente_activado_true(): # El archivo indica que el modo está activo
    contenido = '{"permanente_activado": true}'
    with mock.patch("builtins.open", mock.mock_open(read_data=contenido)), \
         mock.patch("os.path.exists", return_value=True):
        assert estado_permanente_activado() is True

def test_estado_permanente_activado_false_por_archivo_inexistente(): # El archivo no existe
    with mock.patch("os.path.exists", return_value=False):
        assert estado_permanente_activado() is False

def test_estado_permanente_activado_false_por_error_json(): # El archivo existe pero no es un JSON válido
    with mock.patch("builtins.open", mock.mock_open(read_data="{invalido")), \
         mock.patch("os.path.exists", return_value=True):
        assert estado_permanente_activado() is False

def test_modo_permanente_ejecuta_y_se_detiene(): # Verifica que la función se ejecute una vez y luego se detenga
    mock_func = mock.Mock()

    # Primera vez devuelve True, luego False
    with mock.patch("app.planificador.estado_permanente_activado", side_effect=[True, False]), \
         mock.patch("time.sleep"):
        modo_permanente(mock_func, intervalo=0.1)

    # La función debe haberse ejecutado exactamente una vez
    assert mock_func.call_count == 1

def test_modo_temporizador_registra_inicio_y_fin():
    mock_func = mock.Mock()
    tiempos = [0, 0.5, 1.1]  # 2 iteraciones con intervalo ~0.5s

    with mock.patch("app.planificador.time.time", side_effect=tiempos), \
         mock.patch("app.planificador.time.sleep"), \
         mock.patch("app.planificador.registrar_evento_bloqueo") as mock_log:

        modo_temporizador(mock_func, duracion_segundos=1, nombre="block apps")

        mock_log.assert_any_call("sesion", "block apps", None, "iniciada (modo: temporizador, duración: 1s)")
        mock_log.assert_any_call("sesion", "block apps", None, "finalizada")

def test_modo_temporizador_registra_interrupcion():
    def interrumpe(*args, **kwargs):
        raise KeyboardInterrupt

    with mock.patch("app.planificador.time.time", return_value=0), \
         mock.patch("app.planificador.time.sleep"), \
         mock.patch("app.planificador.registrar_evento_bloqueo") as mock_log:

        modo_temporizador(interrumpe, duracion_segundos=1, nombre="block apps")

        mock_log.assert_any_call("sesion", "block apps", None, "iniciada (modo: temporizador, duración: 1s)")
        mock_log.assert_any_call("sesion", "block apps", None, "detenida manualmente")

def test_modo_permanente_registra_inicio_y_fin():
    mock_func = mock.Mock()

    with mock.patch("app.planificador.estado_permanente_activado", side_effect=[True, False]), \
         mock.patch("app.planificador.time.sleep"), \
         mock.patch("app.planificador.registrar_evento_bloqueo") as mock_log:

        modo_permanente(mock_func, intervalo=1, nombre="block apps")

        mock_log.assert_any_call("sesion", "block apps", None, "iniciada (modo: permanente)")
        mock_log.assert_any_call("sesion", "block apps", None, "finalizada")

