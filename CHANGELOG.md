
---

### `CHANGELOG.md`
```markdown
# Changelog
 
Formato basado en [Semantic Versioning](https://semver.org/lang/es/).

---

## [0.1.0] - 2025-07-10
### Added
- Estructura base del proyecto
- Archivos iniciales: README, CHANGELOG, .gitignore

---

## [0.1.1] - 2025-07-11
### Added
- Funciones `obtener_procesos_activos()` y `cerrar_proceso()` en `gestor_procesos.py`
- Tests unitarios para ambas funciones usando `pytest` y `unittest.mock`
- Archivo `pytest.ini` para agregar la raíz del proyecto al `PYTHONPATH`

### Fixed
- Problema de importación en tests solucionado con configuración en `pytest.ini`

---

## [0.1.2] - 2025-07-11
### Added
- Función `bucle_bloqueo_procesos(...)` para ejecutar cierre de procesos durante X segundos
- Función `escanear_y_cerrar_apps(...)` modular y testeable
- Función `ejecutar_con_duracion(...)` para repetir una función con control de tiempo
- Soporte de carga dinámica desde `config.json`
- Tests unitarios con `pytest` y `unittest.mock`
- Test de integración de bucle con conexión completa entre funciones y mocks

### Changed
- Refactor del bucle principal para mejor testabilidad

---

## [0.1.3] - 2025-07-11
### Added
- CLI inicial con Typer en `main.py`
- Comando `block apps` con opciones `--duracion` y `--intervalo`
- Manejo de ejecución sin subcomandos con mensaje personalizado

---

## [0.1.4] - 2025-07-11
### Test
- Test de CLI para `block apps` usando `CliRunner` y `unittest.mock`

---

## [0.1.5] - 2025-07-12
### Added
- Función `bloquear_webs()` para bloquear sitios modificando el archivo hosts
- Función `restaurar_hosts_original()` para revertir cambios en hosts
- Función `flush_dns()` para vaciar caché DNS según sistema operativo

### Test
- Tests de `bloquear_webs()` y `restaurar_hosts_original()` usando mocks
- Test de `flush_dns()` simulando sistema operativo y subprocess

---

## [0.1.6] - 2025-07-12
### Added
- Comando CLI `block websites` para bloquear sitios desde config.json
- Comando CLI `unblock websites` para restaurar el archivo hosts
- Mensaje al usuario recomendando cerrar el navegador para que el bloqueo surta efecto

### Test
- Tests CLI para `block websites` y `unblock websites` usando `CliRunner` y mocks

---

## [0.1.7] - 2025-07-15
### Added
- Función `es_administrador()` para detectar privilegios elevados (Windows)
- Función `reiniciar_como_admin()` que relanza el script con permisos de admin
- Integración en CLI: comandos `block websites` y `unblock websites` ahora piden elevación si es necesario

### Test
- Tests unitarios para `es_administrador()` simulando True, False y excepción
- Tests para `reiniciar_como_admin()` mockeando ejecución y validando comportamiento sin ejecutar UAC real

---

## [0.1.8] - 2025-07-17
### Added
- Se corrige errores en los tests rotos por la implementación de `reiniciar_como_admin()`
- Soporte para el parámetro `--config-path` en `block websites`
- Lógica condicional para omitir `reiniciar_como_admin()` en modo testing
- Tests funcionales de CLI usando archivos reales sin mocks (`config_test.json`)

### Changed
- `config.py` permite cargar configuraciones desde rutas externas

---

## [0.1.9] - 2025-07-17

### Added
- Nuevo módulo `planificador.py` para manejar distintos modos de bloqueo
- Función `modo_temporizador(...)` que ejecuta una función durante un periodo de tiempo determinado, útil para bloqueos temporales
- Soporte de argumentos dinámicos vía `*args` y `**kwargs` para máxima reutilización

### Test
- Test unitario para `modo_temporizador(...)` usando mocks de `time.time` y `time.sleep`
- Validación del número de llamadas a la función pasada

### Docs
- Agregados docstrings explicativos a funciones en `main.py`

---

## [0.1.10] - 2025-07-17

### Added
- Función `parsear_duracion(...)` para interpretar duraciones flexibles como '25m', '2h', '90s' o números
- Compatibilidad con entrada como `int` o `float` (minutos por defecto)

### Test
- Test unitarios para casos válidos y formato inválido

---

## [0.1.11] - 2025-07-17

### Added
- Función `modo_horario(...)` en `planificador.py` que ejecuta acciones si la hora actual está en el rango definido
- Soporte para rangos que cruzan medianoche (ej: 22:00 a 03:00)

### Test
- Test unitarios de `modo_horario` usando mocks de `datetime.now` para simular hora en rango y fuera de rango
- Función auxiliar `_modo_horario_iter(...)` para facilitar pruebas controladas

---