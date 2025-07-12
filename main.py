import typer
from app.gestor_procesos import bucle_bloqueo_procesos
from app.gestor_webs import bloquear_webs, flush_dns, restaurar_hosts_original
from app.config import cargar_configuracion

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
        typer.echo("Bienvenido a LumiBlocker\nUsa 'block apps' para bloquear aplicaciones.")

@block_app.command("apps")
def bloquear_apps(
    duracion: float = typer.Option(10, help="Duración del bloqueo en segundos"),
    intervalo: float = typer.Option(1, help="Intervalo entre escaneos en segundos")
):
    """
    Bloquea las aplicaciones definidas en config.json durante cierto tiempo.
    """
    typer.echo(f"Bloqueando apps por {duracion} segundos (intervalo: {intervalo}s)...")
    bucle_bloqueo_procesos(duracion_segundos=duracion, intervalo=intervalo)


@block_app.command("websites")
def bloquear_websites():
    """
    Bloquea sitios web definidos en config.json modificando el archivo hosts.
    """
    config = cargar_configuracion()
    dominios = config.get("webs_bloqueadas", [])

    if not dominios:
        typer.echo("No hay sitios web definidos para bloquear en config.json.")
        raise typer.Exit()

    typer.echo(f"Bloqueando los siguientes sitios: {', '.join(dominios)}")
    bloquear_webs(dominios)
    flush_dns()

    typer.echo("Sitios bloqueados.")
    typer.echo("Si ya tenías abierta alguna pestaña de estos sitios, cierra y vuelve a abrir tu navegador para aplicar el bloqueo.")

@unblock_app.command("websites")
def desbloquear_websites():
    """
    Restaura el archivo hosts eliminando los sitios bloqueados por LumiBlocker.
    """
    restaurar_hosts_original()
    flush_dns()
    typer.echo("Sitios desbloqueados correctamente.")

if __name__ == "__main__":
    app()