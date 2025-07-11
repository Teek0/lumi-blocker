from app.gestor_procesos import obtener_procesos_activos, cerrar_proceso
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