from utils.parsers import parsear_duracion
import pytest

def test_parsear_duracion_en_segundos():
    assert parsear_duracion("90s") == 90
    assert parsear_duracion("2h") == 7200
    assert parsear_duracion("1.5h") == 5400
    assert parsear_duracion("30m") == 1800
    assert parsear_duracion("2.5m") == 150
    assert parsear_duracion(25) == 1500
    assert parsear_duracion(1.5) == 90
    assert parsear_duracion("45") == 2700  # default: minutos

def test_parsear_duracion_formato_invalido():
    with pytest.raises(ValueError):
        parsear_duracion("xd")
