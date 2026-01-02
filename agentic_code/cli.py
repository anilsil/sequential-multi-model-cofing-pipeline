"""
CLI interface for agentic-code (Prompt Orchestrator).

Commands: run

No API keys needed - this tool generates prompts for you to use with free AI tools!
"""

from pathlib import Path
from typing import Optional
import sys

import typer
from rich.console import Console
from rich.panel import Panel

from . import __version__
from .config import Config, load_config, validate_config
from .pipeline import AgenticPipeline
from .automated_pipeline import AutomatedAgenticPipeline
from .utils import print_section

# Initialize Typer app
app = typer.Typer(
    name="agentic-code",
    help="Local-first, governed multi-model agentic coding pipeline (100% FREE - Prompt Orchestrator)",
    add_completion=False,
)

console = Console()


@app.command()
def run(
    task_file: str = typer.Argument(
        ...,
        help="Path to task specification file (.md, .yaml, or .json)"
    ),
    automated: bool = typer.Option(
        False,
        "--automated",
        help="Run in automated mode (requires API keys)"
    ),
    skip_verification: bool = typer.Option(
        False,
        "--skip-verification",
        help="Skip Gemini verification stage"
    ),
    output_dir: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output directory for artifacts (default: ./output)"
    ),
    test_mode: bool = typer.Option(
        False,
        "--test-mode",
        help="Run in test mode (simulate API responses and auto-confirmations)"
    ),
):
    """
    Run the agentic coding pipeline on a task.

    The pipeline can be run in two modes:
    1. Prompt-based (default): Generates prompts for you to use with free AI tools.
    2. Automated: Runs the pipeline automatically using API calls, with human review at each stage.
    """
    if automated:
        print_section(f"🚀 AGENTIC-CODE v{__version__} (Automated Pipeline)", style="cyan")
    else:
        print_section(f"🚀 AGENTIC-CODE v{__version__} (FREE Prompt Orchestrator)", style="cyan")

    # Load configuration
    config = load_config(
        output_dir=Path(output_dir) if output_dir else None
    )

    # Override with CLI flags
    config.skip_verification = skip_verification
    config.test_mode = test_mode

    # Validate configuration
    errors = validate_config(config)
    if errors:
        console.print("[red bold]Configuration errors:[/red bold]")
        for error in errors:
            console.print(f"  [red]✗[/red] {error}")
        sys.exit(1)

    # Validate task file
    task_path = Path(task_file)
    if not task_path.exists():
        console.print(f"[red]Task file not found: {task_path}[/red]")
        sys.exit(1)

    # Create output directory
    config.output_dir.mkdir(parents=True, exist_ok=True)

    # Print configuration summary
    console.print("[dim]Configuration:[/dim]")
    console.print(f"[dim]  Task: {task_path}[/dim]")
    console.print(f"[dim]  Output: {config.output_dir}[/dim]")
    console.print(f"[dim]  Skip verification: {config.skip_verification}[/dim]")
    if automated:
        console.print(f"[dim]  Mode: Automated (API calls with human review)[/dim]")
    else:
        console.print(f"[dim]  Mode: 100% FREE - Prompt-based (no API calls)[/dim]")
    console.print()

    try:
        # Select and run pipeline
        if automated:
            pipeline = AutomatedAgenticPipeline(config)
        else:
            pipeline = AgenticPipeline(config)
        
        results = pipeline.run(task_path)

        # Exit with appropriate code
        status = results.get("status", "unknown")
        if status == "completed":
            decision = results.get("final_decision", "UNKNOWN")
            if decision == "APPROVE":
                console.print("\n[green bold]✓ Pipeline completed - Code approved for integration[/green bold]\n")
                sys.exit(0)
            elif decision == "APPROVE_WITH_NOTES":
                console.print("\n[yellow bold]⚠ Pipeline completed - Code approved with notes[/yellow bold]\n")
                sys.exit(0)
            elif decision == "REJECT":
                console.print("\n[red bold]✗ Pipeline completed - Code rejected, fixes required[/red bold]\n")
                sys.exit(1)
            else:
                console.print("\n[yellow]Pipeline completed[/yellow]\n")
                sys.exit(0)
        elif "cancelled" in status:
            console.print("\n[yellow]Pipeline cancelled by user[/yellow]\n")
            sys.exit(0)
        else:
            console.print(f"\n[red]Pipeline failed: {status}[/red]\n")
            sys.exit(1)

    except KeyboardInterrupt:
        console.print("\n\n[yellow]Interrupted by user[/yellow]")
        sys.exit(130)
    except Exception as e:
        console.print(f"\n[red bold]Fatal error: {e}[/red bold]")
        import traceback
        traceback.print_exc()
        sys.exit(1)


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
        False,
        "--version",
        "-v",
        help="Show version and exit"
    )
):
    """
    Agentic Code - Local-first, governed multi-model coding pipeline.

    Modes:
    - Default: 🆓 100% FREE - Generates prompts for free AI tools (Claude Code CLI, Cursor, Gemini)
    - --automated: Requires API keys and provides a fully automated pipeline with human review.

    Run 'agentic-code --help' for available commands.
    """
    if version_flag:
        console.print(f"[bold cyan]agentic-code[/bold cyan] version [green]{__version__}[/green]")
        console.print(f"[dim]Default Mode: Prompt Orchestrator (100% FREE)[/dim]")
        console.print(f"[dim]Automated Mode: --automated (requires API keys)[/dim]")
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        console.print(Panel(
            "[bold]Agentic Code - Local-first Pipeline[/bold]\n\n"
            "Modes of Operation:\n"
            "  [bold]Default (Prompt-based):[/bold] 🆓 100% FREE - No API costs!\n"
            "  Generates prompts for free AI tools:\n"
            "    • Claude Code CLI (planning & decisions)\n"
            "    • Cursor/Copilot (implementation)\n"
            "    • Gemini (optional verification)\n\n"
            "  [bold]Automated:[/bold] (--automated)\n"
            "  Runs the full pipeline with API calls, prompting you for a 'yes/no' review at each stage. Requires API keys.\n\n"
            "  [bold]Test Mode:[/bold] (--test-mode)\n"
            "  Can be combined with --automated. Simulates API responses and auto-confirms human actions for faster testing.\n\n"
            "Commands:\n"
            "  [cyan]run[/cyan]       Run pipeline on a task\n"
            "  [cyan]version[/cyan]   Show version\n\n"
            "Run [bold]agentic-code run --help[/bold] for more info\n\n"
            "[dim]Example: agentic-code run examples/simple-function.md --automated --test-mode[/dim]",
            title="🤖 Agentic Code",
            border_style="cyan"
        ))


if __name__ == "__main__":
    app()
