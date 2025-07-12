import typer
from app.gestor_procesos import bucle_bloqueo_procesos

app = typer.Typer(help="LumiBlocker CLI - Controla tu enfoque bloqueando distracciones")

# Subgrupo de comandos: block
block_app = typer.Typer(help="Comandos para bloquear elementos (apps, websites, etc.)")
app.add_typer(block_app, name="block")

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

if __name__ == "__main__":
    app()