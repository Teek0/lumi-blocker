from app.gestor_procesos import obtener_procesos_activos, cerrar_proceso, escanear_y_cerrar_apps, ejecutar_con_duracion, bucle_bloqueo_procesos
from unittest.mock import patch, MagicMock

# Tests for obtener_procesos_activos
def test_obtener_procesos_activos_retorna_lista():
    procesos = obtener_procesos_activos()
    assert isinstance(procesos, list)

def test_obtener_procesos_activos_no_esta_vacia():
    procesos = obtener_procesos_activos()
    assert len(procesos) > 0 # debería haber al menos el proceso de Python ejecutándose

# Tests for cerrar_proceso
def test_cerrar_proceso_nombre_existente():
    mock_proc = MagicMock()
    mock_proc.info = {'name': 'Notepad.exe', 'pid': 12345}

    with patch('psutil.process_iter', return_value=[mock_proc]):
        cerrados = cerrar_proceso('Notepad.exe')
        assert cerrados == [12345]  # debería cerrar el proceso y retornar su PID
        mock_proc.terminate.assert_called_once()

def test_cerrar_proceso_nombre_inexistente():
    mock_proc = MagicMock()
    mock_proc.info = {'name': 'explorer.exe', 'pid': 99999}

    with patch('psutil.process_iter', return_value=[mock_proc]):
        cerrados = cerrar_proceso('Notepad.exe')
        assert cerrados == []
        mock_proc.terminate.assert_not_called()

# Tests for escanear_y_cerrar_apps
def test_escanear_y_cerrar_apps_cierra_procesos_simulados():
    mock_proc = MagicMock()
    mock_proc.info = {'name': 'notepad.exe', 'pid': 1234}

    with patch('app.gestor_procesos.obtener_procesos_activos', return_value=['notepad.exe']):
        with patch('app.gestor_procesos.cerrar_proceso', return_value=[1234]) as mock_cerrar:
            resultado = escanear_y_cerrar_apps(['notepad.exe'])
            assert resultado == {'notepad.exe': [1234]}
            mock_cerrar.assert_called_once_with('notepad.exe')

def test_escanear_y_cerrar_apps_no_cierra_nada_si_no_activa():
    with patch('app.gestor_procesos.obtener_procesos_activos', return_value=['steam.exe']):
        with patch('app.gestor_procesos.cerrar_proceso') as mock_cerrar:
            resultado = escanear_y_cerrar_apps(['notepad.exe'])
            assert resultado == {}
            mock_cerrar.assert_not_called()

# Tests for ejecutar_con_duracion
def test_ejecutar_con_duracion_llama_funcion_correctamente():
    mock_func = MagicMock()
    # Simular tiempo progresivo: 0 → 1 → 2 → 3 (3 iteraciones con intervalo 1)
    tiempos_simulados = [0, 1, 2, 3]

    with patch('app.gestor_procesos.time.time', side_effect=tiempos_simulados):
        with patch('app.gestor_procesos.time.sleep'):
            ejecutar_con_duracion(mock_func, duracion=2.5, intervalo=1)
    
    assert mock_func.call_count == 2

# Tests for bucle_bloqueo_procesos
def test_bucle_bloqueo_procesos_conecta_todo_correctamente():
    config_falsa = {"apps_bloqueadas": ["notepad.exe"]}

    with patch('app.gestor_procesos.cargar_configuracion', return_value=config_falsa):
        with patch('app.gestor_procesos.ejecutar_con_duracion') as mock_ejecutar:
            bucle_bloqueo_procesos(duracion_segundos=1, intervalo=1)

            mock_ejecutar.assert_called_once()

            # Verificamos que la función pasada como tarea sea callable
            tarea_llamada = mock_ejecutar.call_args[0][0]
            assert callable(tarea_llamada)

            # Simulamos una ejecución directa para validar el contenido
            with patch('app.gestor_procesos.escanear_y_cerrar_apps', return_value={'notepad.exe': [1234]}) as mock_escaneo:
                tarea_llamada()  # Ejecutamos la tarea como en el bucle
                mock_escaneo.assert_called_once_with(["notepad.exe"])

def test_cerrar_proceso_ignora_proceso_protegido():
    mock_proc = MagicMock()
    mock_proc.info = {'name': 'explorer.exe', 'pid': 1111}
    mock_proc.name.return_value = 'explorer.exe'  # nombre real del proceso para verificación
    mock_proc.pid = 1111

    with patch('psutil.process_iter', return_value=[mock_proc]):
        cerrados = cerrar_proceso('explorer.exe')
        assert cerrados == []  # explorer.exe está en PROCESOS_PROTEGIDOS
        mock_proc.terminate.assert_not_called()


def test_cerrar_proceso_ignora_pid_actual():
    import os
    mock_proc = MagicMock()
    mock_proc.info = {'name': 'notepad.exe', 'pid': os.getpid()}
    mock_proc.name.return_value = 'notepad.exe'
    mock_proc.pid = os.getpid()

    with patch('psutil.process_iter', return_value=[mock_proc]):
        cerrados = cerrar_proceso('notepad.exe')
        assert cerrados == []  # no debería cerrarse a sí mismo
        mock_proc.terminate.assert_not_called()