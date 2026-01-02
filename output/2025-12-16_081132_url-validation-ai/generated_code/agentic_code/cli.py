"""
CLI interface for agentic-code (Prompt Orchestrator) plus URL analysis helpers.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

console = Console()

try:
    from . import __version__
except Exception:  # pragma: no cover
    __version__ = "0.0.0"

try:  # Optional pipeline imports; degrade gracefully if not present
    from .config import Config, load_config, validate_config
    from .pipeline import AgenticPipeline
except Exception:  # pragma: no cover
    Config = None
    load_config = None
    validate_config = None
    AgenticPipeline = None

from .url_analyzer import URLAnalyzer, render_analysis_table
from .url_database import URLAnalysisDB
from .url_extractor import extract_urls

try:
    from .utils import print_section
except Exception:  # pragma: no cover
    def print_section(message: str, style: str | None = None) -> None:
        console.print(message)

app = typer.Typer(
    name="agentic-code",
    help="Local-first, governed multi-model agentic coding pipeline",
    add_completion=False,
)


@app.command()
def run(
    task_file: str = typer.Argument(..., help="Path to task specification file"),
    skip_verification: bool = typer.Option(
        False, "--skip-verification", help="Skip Gemini verification stage"
    ),
    output_dir: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output directory for artifacts (default: ./output)",
    ),
):
    """
    Run the agentic coding pipeline on a task.
    """
    if not AgenticPipeline or not load_config or not validate_config:
        console.print(
            "[red]Pipeline modules unavailable in generated_code build.[/red]"
        )
        raise typer.Exit(code=1)

    print_section(f"🚀 AGENTIC-CODE v{__version__}", style="cyan")

    config = load_config(output_dir=Path(output_dir) if output_dir else None)
    config.skip_verification = skip_verification

    errors = validate_config(config)
    if errors:
        console.print("[red bold]Configuration errors:[/red bold]")
        for error in errors:
            console.print(f"  [red]✗[/red] {error}")
        raise typer.Exit(code=1)

    task_path = Path(task_file)
    if not task_path.exists():
        console.print(f"[red]Task file not found: {task_path}[/red]")
        raise typer.Exit(code=1)

    config.output_dir.mkdir(parents=True, exist_ok=True)

    console.print("[dim]Configuration:[/dim]")
    console.print(f"[dim]  Task: {task_path}[/dim]")
    console.print(f"[dim]  Output: {config.output_dir}[/dim]")
    console.print(f"[dim]  Skip verification: {config.skip_verification}[/dim]")
    console.print(f"[dim]  Mode: Prompt-based (no API calls)[/dim]")
    console.print()

    pipeline = AgenticPipeline(config)
    results = pipeline.run(task_path)
    status = results.get("status", "unknown")
    if status == "completed":
        console.print("[green]Pipeline completed[/green]")
        raise typer.Exit(code=0)
    raise typer.Exit(code=1)


@app.command("analyze-url")
def analyze_url(
    text_or_url: str = typer.Argument(..., help="URL or text containing URLs"),
    save: bool = typer.Option(True, help="Persist results to SQLite database"),
):
    """
    Analyze a single URL or extract URLs from provided text.
    """
    analyzer = URLAnalyzer()
    db = URLAnalysisDB()

    urls = extract_urls(text_or_url)
    if not urls:
        urls = [text_or_url]

    results = analyzer.batch_analyze(urls, save=save, db=db)
    render_analysis_table(results)


@app.command("batch-analyze")
def batch_analyze(
    file_path: str = typer.Argument(..., help="Path to file with URLs/text"),
    save: bool = typer.Option(True, help="Persist results to SQLite database"),
):
    """
    Analyze URLs from a file (one URL per line or free-form text).
    """
    path = Path(file_path)
    if not path.exists() or not path.is_file():
        console.print(f"[red]File not found: {file_path}[/red]")
        raise typer.Exit(code=1)

    content = path.read_text(encoding="utf-8")
    analyzer = URLAnalyzer()
    db = URLAnalysisDB()
    results = analyzer.analyze_text(content, save=save, db=db)
    render_analysis_table(results)


@app.command("add-to-blacklist")
def add_to_blacklist(domain: str = typer.Argument(..., help="Domain to blacklist")):
    """
    Add a domain to the blacklist data file.
    """
    if not re.fullmatch(r"[A-Za-z0-9.-]+", domain):
        console.print("[red]Invalid domain format[/red]")
        raise typer.Exit(code=1)

    analyzer = URLAnalyzer()
    blacklist_file = analyzer.data_dir / "blacklist_domains.txt"
    if blacklist_file.exists():
        blacklist = {
            line.strip().lower()
            for line in blacklist_file.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
    else:
        blacklist = set()

    if domain.lower() in blacklist:
        console.print("[yellow]Domain already blacklisted[/yellow]")
        raise typer.Exit(code=0)

    with blacklist_file.open("a", encoding="utf-8") as fh:
        fh.write(f"{domain.lower()}\n")

    console.print(f"[green]Added {domain} to blacklist[/green]")


@app.command()
def version():
    """
    Show version information.
    """
    console.print(f"[bold cyan]agentic-code[/bold cyan] version [green]{__version__}[/green]")
    console.print(f"[dim]Mode: Prompt Orchestrator (100% FREE - No API costs!)[/dim]")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version_flag: bool = typer.Option(
        False, "--version", "-v", help="Show version and exit"
    ),
):
    """
    Agentic Code - Local-first, governed multi-model coding pipeline.
    """
    if version_flag:
        console.print(f"[bold cyan]agentic-code[/bold cyan] version [green]{__version__}[/green]")
        console.print(f"[dim]Mode: Prompt Orchestrator (100% FREE)[/dim]")
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        console.print(
            Panel(
                "[bold]Agentic Code - Prompt Orchestrator[/bold]\n\n"
                "Commands:\n"
                "  [cyan]run[/cyan]              Run pipeline on a task\n"
                "  [cyan]analyze-url[/cyan]      Analyze a URL or text\n"
                "  [cyan]batch-analyze[/cyan]    Analyze URLs from file\n"
                "  [cyan]add-to-blacklist[/cyan] Add domain to blacklist\n"
                "  [cyan]version[/cyan]          Show version\n\n"
                "[dim]Example: agentic-code analyze-url \"Check https://example.com\"[/dim]",
                title="🤖 Agentic Code",
                border_style="cyan",
            )
        )


if __name__ == "__main__":
    app()
