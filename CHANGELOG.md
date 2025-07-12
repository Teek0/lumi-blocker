
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

## [0.1.1] - 2025-07-10
### Added
- Funciones `obtener_procesos_activos()` y `cerrar_proceso()` en `gestor_procesos.py`
- Tests unitarios para ambas funciones usando `pytest` y `unittest.mock`
- Archivo `pytest.ini` para agregar la raíz del proyecto al `PYTHONPATH`

### Fixed
- Problema de importación en tests solucionado con configuración en `pytest.ini`

---

## [0.1.2] - 2025-07-10
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

## [0.1.3] - 2025-07-10
### Added
- CLI inicial con Typer en `main.py`
- Comando `block apps` con opciones `--duracion` y `--intervalo`
- Manejo de ejecución sin subcomandos con mensaje personalizado

---

