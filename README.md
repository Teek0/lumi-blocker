# 🧠 LumiBlocker

Aplicación local para bloquear aplicaciones y sitios web según reglas personalizadas.

## Objetivo
Apoyar el enfoque y el bienestar digital bloqueando distracciones comunes (Steam, YouTube, etc.)

## Características iniciales
- Bloqueo de procesos por nombre
- Bloqueo de sitios mediante `hosts`
- Configuración de horarios y persistencia
- CLI con Typer

---

### 🚀 Lanzar el proyecto

1. Asegúrate de tener Python 3.10+ instalado.
2. Instala las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

3. Ejecuta la aplicación desde la raíz del proyecto:

```bash
python main.py
```

También puedes usar subcomandos directamente:

```bash
python main.py block apps
```

---

## 🛠 Comandos disponibles

### 🔒 `block apps`

Bloquea procesos de aplicaciones definidos en `config.json` (campo `apps_bloqueadas`).

```bash
python main.py block apps --modo [temporizador|horario|permanente] [opciones]
```

#### Opciones por modo:

- `--modo`: modo de bloqueo (`temporizador`, `horario`, `permanente`)
- `--duracion`: duración en formatos como `25m`, `1h` (solo para `temporizador`)
- `--inicio`: hora inicio en formato `HH:MM` (solo para `horario`)
- `--fin`: hora fin en formato `HH:MM` (solo para `horario`)
- `--intervalo`: intervalo entre chequeos, en segundos (por defecto: `1`)

#### Ejemplos:

```bash
python main.py block apps --modo temporizador --duracion 25m
python main.py block apps --modo horario --inicio 09:00 --fin 12:00
python main.py block apps --modo permanente
```

---

### 🌐 `block websites`

Bloquea sitios web editando el archivo `hosts`. Usa las webs definidas en `config.json` (campo `webs_bloqueadas`).

```bash
python main.py block websites --modo [temporizador|horario|permanente] [opciones]
```

#### Opciones:

- `--modo`: modo de bloqueo (`temporizador`, `horario`, `permanente`)
- `--duracion`: duración como `30m`, `1.5h` (solo para `temporizador`)
- `--inicio`: hora inicio `HH:MM` (solo para `horario`)
- `--fin`: hora fin `HH:MM` (solo para `horario`)
- `--intervalo`: intervalo entre chequeos DNS, por defecto `60`
- `--config-path`: ruta al archivo de configuración (por defecto: `config.json`)

> ⚠️ Requiere ejecutar como administrador para modificar el archivo `hosts`.

#### Ejemplos:

```bash
python main.py block websites --modo temporizador --duracion 45m
python main.py block websites --modo horario --inicio 08:30 --fin 11:00
python main.py block websites --modo permanente
```

---

### 🔓 `unblock websites`

Restaura el archivo `hosts` y elimina los sitios bloqueados por LumiBlocker.

```bash
python main.py unblock websites
```

> También requiere privilegios de administrador.

---

## 📂 Archivos clave

- `config.json`: define `apps_bloqueadas` y `webs_bloqueadas`.
- `estado_bloqueo.json`: controla si el bloqueo permanente está activo.
- `logs.json`: registra sesiones, errores y eventos.