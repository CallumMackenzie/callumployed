import typer

app = typer.Typer(help="Local-first job-search automation CLI.")


@app.callback()
def main() -> None:
    """Manage target companies, roles, applications, and job-search artifacts."""
