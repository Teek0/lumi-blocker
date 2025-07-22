import typer
from typing import Literal, Optional
from app.gestor_procesos import bucle_bloqueo_procesos
from app.gestor_webs import bloquear_webs, flush_dns, restaurar_hosts_original
from utils.permisos import reiniciar_como_admin
from app.config import cargar_configuracion
from app.planificador import modo_temporizador, modo_horario, modo_permanente
from utils.parsers import parsear_duracion

MODOS_DISPONIBLES = ["temporizador", "horario", "permanente"]

app = typer.Typer(help="LumiBlocker CLI - Controla tu enfoque bloqueando distracciones")

# Subgrupo de comandos: block
block_app = typer.Typer(help="Comandos para bloquear elementos (apps, websites, etc.)")
app.add_typer(block_app, name="block")
unblock_app = typer.Typer(help="Comandos para desbloquear elementos previamente bloqueados")
app.add_typer(unblock_app, name="unblock")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Bienvenido a LumiBlocker
    Usa subcomandos como 'block apps' para comenzar.
    """
    if ctx.invoked_subcommand is None:
        typer.echo("Bienvenido a LumiBlocker\\nUsa 'block apps' para bloquear aplicaciones.")

@block_app.command("apps")
def bloquear_apps(
    modo: str = typer.Option(
    "temporizador",
    help="Modo de bloqueo",
    show_choices=True,
    metavar=f"{MODOS_DISPONIBLES}",
),
    duracion: Optional[str] = typer.Option(None, help="Duración (solo para modo temporizador). Ej: 25m, 1.5h"),
    inicio: Optional[str] = typer.Option(None, help="Hora inicio (HH:MM, solo para modo horario)"),
    fin: Optional[str] = typer.Option(None, help="Hora fin (HH:MM, solo para modo horario)"),
    intervalo: float = typer.Option(1, help="Intervalo entre escaneos en segundos")
):
    """
    Bloquea las aplicaciones definidas en config.json, con modo a elección: temporizador, horario o permanente.
    """
    if modo not in MODOS_DISPONIBLES:
        typer.echo(f"Modo inválido: {modo}. Debe ser uno de {MODOS_DISPONIBLES}.")
        raise typer.Exit()
    from app.config import cargar_configuracion
    from app.gestor_procesos import bucle_bloqueo_procesos

    config = cargar_configuracion()
    apps_bloqueadas = config.get("apps_bloqueadas", [])

    if not apps_bloqueadas:
        typer.echo("No hay apps definidas para bloquear.")
        raise typer.Exit()

    def funcion_bloqueo():
        bucle_bloqueo_procesos(duracion_segundos=1, intervalo=intervalo)

    if modo == "temporizador":
        if not duracion:
            typer.echo("Debes especificar una duración para el modo temporizador.")
            raise typer.Exit()
        segundos = parsear_duracion(duracion)
        modo_temporizador(funcion_bloqueo, duracion_segundos=segundos)

    elif modo == "horario":
        if not inicio or not fin:
            typer.echo("Debes especificar --inicio y --fin en formato HH:MM para el modo horario.")
            raise typer.Exit()
        modo_horario(funcion_bloqueo, hora_inicio=inicio, hora_fin=fin, intervalo=int(intervalo))

    elif modo == "permanente":
        modo_permanente(funcion_bloqueo, intervalo=int(intervalo))

@block_app.command("websites")
def bloquear_websites(
    modo: str = typer.Option(
    "temporizador",
    help="Modo de bloqueo",
    show_choices=True,
    metavar=f"{MODOS_DISPONIBLES}",
),
    duracion: Optional[str] = typer.Option(None, help="Duración (solo para modo temporizador). Ej: 30m, 1h"),
    inicio: Optional[str] = typer.Option(None, help="Hora inicio (HH:MM, solo para modo horario)"),
    fin: Optional[str] = typer.Option(None, help="Hora fin (HH:MM, solo para modo horario)"),
    intervalo: float = typer.Option(60, help="Intervalo entre chequeos en segundos"),
    config_path: str = "config.json"
):
    """
    Bloquea sitios web definidos en config.json mediante modificación del archivo hosts.
    Soporta modos: temporizador, horario, permanente.
    """
    if modo not in MODOS_DISPONIBLES:
        typer.echo(f"Modo inválido: {modo}. Debe ser uno de {MODOS_DISPONIBLES}.")
        raise typer.Exit()
    import os
    if not os.environ.get("TESTING"):
        reiniciar_como_admin()

    from app.gestor_webs import bloquear_webs, flush_dns
    from app.config import cargar_configuracion

    config = cargar_configuracion(config_path)
    dominios = config.get("webs_bloqueadas", [])

    if not dominios:
        typer.echo("No hay sitios web definidos para bloquear en config.json.")
        raise typer.Exit()

    def funcion_bloqueo():
        bloquear_webs(dominios)
        flush_dns()

    if modo == "temporizador":
        if not duracion:
            typer.echo("Debes especificar una duración para el modo temporizador.")
            raise typer.Exit()
        segundos = parsear_duracion(duracion)
        modo_temporizador(funcion_bloqueo, duracion_segundos=segundos)

    elif modo == "horario":
        if not inicio or not fin:
            typer.echo("Debes especificar --inicio y --fin en formato HH:MM para el modo horario.")
            raise typer.Exit()
        modo_horario(funcion_bloqueo, hora_inicio=inicio, hora_fin=fin, intervalo=int(intervalo))

    elif modo == "permanente":
        modo_permanente(funcion_bloqueo, intervalo=int(intervalo))

@unblock_app.command("websites")
def desbloquear_websites():
    """
    Restaura el archivo hosts eliminando los sitios bloqueados por LumiBlocker.
    """
    import os
    if not os.environ.get("TESTING"):
        reiniciar_como_admin()
    restaurar_hosts_original()
    flush_dns()
    typer.echo("Sitios desbloqueados correctamente.")

if __name__ == "__main__":
    app()