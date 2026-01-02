"""
Utility functions for agentic-code.

Helpers for artifact management, logging, and user interaction.
"""

import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.prompt import Confirm

console = Console()


def create_run_directory(output_dir: Path, task_name: str) -> Path:
    """
    Create a timestamped directory for a pipeline run.

    Args:
        output_dir: Base output directory
        task_name: Name of the task (sanitized for filesystem)

    Returns:
        Path to the created run directory
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    sanitized_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in task_name)
    run_dir = output_dir / f"{timestamp}_{sanitized_name}"
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def save_artifact(
    run_dir: Path,
    filename: str,
    content: str | Dict[str, Any],
    artifact_type: str = "text"
) -> Path:
    """
    Save an artifact to the run directory.

    Args:
        run_dir: Directory for this pipeline run
        filename: Name of the artifact file
        content: Content to save (string or dict for JSON/YAML)
        artifact_type: Type of artifact (text, json, yaml, code)

    Returns:
        Path to the saved artifact
    """
    file_path = run_dir / filename

    if artifact_type == "json" or (isinstance(content, dict) and filename.endswith(".json")):
        file_path.write_text(json.dumps(content, indent=2))
    elif artifact_type == "yaml" or (isinstance(content, dict) and filename.endswith((".yaml", ".yml"))):
        file_path.write_text(yaml.dump(content, default_flow_style=False, sort_keys=False))
    else:
        file_path.write_text(str(content))

    console.print(f"[dim]📝 Artifact saved: {file_path}[/dim]")
    return file_path


def load_task_file(task_path: Path) -> Dict[str, Any]:
    """
    Load a task specification file (supports .md, .yaml, .json).

    Args:
        task_path: Path to task file

    Returns:
        Dictionary with task specification
    """
    if not task_path.exists():
        raise FileNotFoundError(f"Task file not found: {task_path}")

    content = task_path.read_text()
    suffix = task_path.suffix.lower()

    if suffix == ".json":
        return json.loads(content)
    elif suffix in (".yaml", ".yml"):
        return yaml.safe_load(content)
    elif suffix == ".md":
        # Parse markdown as simple task description
        return {
            "name": task_path.stem,
            "description": content,
            "requirements": [],
            "constraints": []
        }
    else:
        raise ValueError(f"Unsupported task file format: {suffix}")


def print_section(title: str, content: str = "", style: str = "blue") -> None:
    """
    Print a formatted section header with optional content.

    Args:
        title: Section title
        content: Optional content to display
        style: Rich color style
    """
    if content:
        console.print(Panel(content, title=title, border_style=style))
    else:
        console.print(f"\n[{style} bold]{'='*60}[/{style} bold]")
        console.print(f"[{style} bold]{title}[/{style} bold]")
        console.print(f"[{style} bold]{'='*60}[/{style} bold]\n")


def print_code(code: str, language: str = "python", title: Optional[str] = None) -> None:
    """
    Print syntax-highlighted code.

    Args:
        code: Code to display
        language: Programming language for syntax highlighting
        title: Optional title for the code block
    """
    syntax = Syntax(code, language, theme="monokai", line_numbers=True)
    if title:
        console.print(Panel(syntax, title=title, border_style="cyan"))
    else:
        console.print(syntax)


def print_findings(findings: list[Dict[str, Any]]) -> None:
    """
    Print verification findings in a formatted table.

    Args:
        findings: List of finding dictionaries with severity, message, etc.
    """
    if not findings:
        console.print("[green]✓ No issues found[/green]")
        return

    table = Table(title="Verification Findings", show_header=True, header_style="bold magenta")
    table.add_column("Severity", style="cyan", width=10)
    table.add_column("Category", style="yellow", width=15)
    table.add_column("Issue", style="white")
    table.add_column("Suggestion", style="green")

    severity_colors = {
        "HIGH": "[red bold]",
        "MEDIUM": "[yellow]",
        "LOW": "[blue]",
    }

    for finding in findings:
        severity = finding.get("severity", "MEDIUM")
        color = severity_colors.get(severity, "")
        table.add_row(
            f"{color}{severity}[/]",
            finding.get("category", "General"),
            finding.get("message", ""),
            finding.get("suggestion", "")
        )

    console.print(table)


def confirm_action(message: str, default: bool = False, test_mode: bool = False) -> bool:
    """
    Prompt user for confirmation.

    Args:
        message: Confirmation message
        default: Default value if user just hits enter
        test_mode: If True, automatically confirms action

    Returns:
        True if user confirms, False otherwise
    """
    if test_mode:
        console.print(f"[dim]Auto-confirming: {message} -> Yes[/dim]")
        return True
    return Confirm.ask(message, default=default)


def print_artifact_summary(run_dir: Path) -> None:
    """
    Print a summary of artifacts created in a run.

    Args:
        run_dir: Directory containing run artifacts
    """
    console.print("\n[bold cyan]📦 Artifacts Created:[/bold cyan]")

    artifacts = sorted(run_dir.glob("*"))
    if not artifacts:
        console.print("[dim]No artifacts found[/dim]")
        return

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("File", style="cyan")
    table.add_column("Size", justify="right", style="green")
    table.add_column("Modified", style="yellow")

    for artifact in artifacts:
        if artifact.is_file():
            size = artifact.stat().st_size
            size_str = f"{size:,} bytes" if size < 1024 else f"{size/1024:.1f} KB"
            mtime = datetime.fromtimestamp(artifact.stat().st_mtime).strftime("%H:%M:%S")
            table.add_row(artifact.name, size_str, mtime)

    console.print(table)
    console.print(f"\n[dim]Run directory: {run_dir}[/dim]\n")


def print_pipeline_status(stage: str, status: str = "running") -> None:
    """
    Print pipeline stage status.

    Args:
        stage: Name of the pipeline stage
        status: Status (running, completed, failed, waiting)
    """
    status_icons = {
        "running": "⏳",
        "completed": "✓",
        "failed": "✗",
        "waiting": "⏸",
    }

    status_colors = {
        "running": "yellow",
        "completed": "green",
        "failed": "red",
        "waiting": "blue",
    }

    icon = status_icons.get(status, "○")
    color = status_colors.get(status, "white")
    console.print(f"[{color}]{icon} {stage}[/{color}]")


def format_duration(seconds: float) -> str:
    """
    Format a duration in seconds to human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted string (e.g., "2m 15s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}m {secs}s"
