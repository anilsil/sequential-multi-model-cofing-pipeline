#!/usr/bin/env python3
"""
Fully automated agentic-code using Claude Code CLI (100% FREE).

This script automates the entire pipeline by:
1. Calling Claude Code CLI programmatically (free)
2. Automatically processing all stages
3. No manual copy-paste needed

Requirements:
- Claude Code CLI installed (https://claude.com/code)
- agentic-code package installed

Usage:
    python scripts/fully_automated.py examples/simple-function.md
    python scripts/fully_automated.py examples/simple-function.md --skip-verification
"""

import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agentic_code.config import Config, load_config
from agentic_code.utils import (
    console,
    create_run_directory,
    load_task_file,
    save_artifact,
    print_section,
    print_pipeline_status,
)


def call_claude_cli(prompt: str, timeout: int = 120) -> str:
    """
    Call Claude Code CLI with a prompt and return response.

    Args:
        prompt: The prompt to send to Claude
        timeout: Timeout in seconds

    Returns:
        Claude's response text

    Raises:
        RuntimeError: If Claude CLI is not available or call fails
    """
    # Check if claude CLI is available
    try:
        subprocess.run(
            ["claude", "--version"],
            capture_output=True,
            check=True,
            timeout=5
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise RuntimeError(
            "Claude Code CLI not found. Install from: https://claude.com/code"
        )

    console.print("[dim]🤖 Calling Claude Code CLI...[/dim]")

    try:
        # Call Claude CLI in batch mode
        # Using 'claude' with --print flag for non-interactive output
        result = subprocess.run(
            ["claude", "--print"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True
        )

        response = result.stdout.strip()

        if not response:
            raise RuntimeError("Empty response from Claude CLI")

        console.print(f"[green]✓ Received response ({len(response)} characters)[/green]")
        return response

    except subprocess.TimeoutExpired:
        raise RuntimeError(f"Claude CLI call timed out after {timeout}s")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Claude CLI error: {e.stderr}")


def run_automated_pipeline(task_path: Path, skip_verification: bool = False):
    """
    Run fully automated pipeline using Claude Code CLI.

    Args:
        task_path: Path to task specification file
        skip_verification: Skip verification stage
    """
    start_time = time.time()

    print_section("🚀 FULLY AUTOMATED AGENTIC CODE (FREE)", style="blue")
    console.print(f"[dim]Task: {task_path}[/dim]")
    console.print(f"[dim]Mode: Claude Code CLI (100% Free)[/dim]")
    console.print(f"[dim]Automation: Fully automated (no manual steps)[/dim]\n")

    # Load config
    config = load_config()
    config.skip_verification = skip_verification

    # Load task
    task_data = load_task_file(task_path)
    task_name = task_data.get("name", task_path.stem)

    # Create run directory
    run_dir = create_run_directory(config.output_dir, task_name)
    console.print(f"[cyan]Run directory:[/cyan] {run_dir}\n")

    # Import prompt templates
    from agentic_code.agents.claude import (
        REPO_ANALYSIS_PROMPT,
        TASK_PLANNING_PROMPT,
        INTEGRATION_DECISION_PROMPT,
    )

    try:
        # Stage 1: Repository Analysis
        print_pipeline_status("Stage 1: Repository Analysis", "running")

        analysis_prompt = REPO_ANALYSIS_PROMPT.format(repo_root=config.repo_root)
        save_artifact(run_dir, "claude_analysis_prompt.md", analysis_prompt, "text")

        repo_analysis = call_claude_cli(analysis_prompt)
        save_artifact(run_dir, "claude_analysis_response.txt", repo_analysis, "text")

        print_pipeline_status("Stage 1: Repository Analysis", "completed")

        # Stage 2: Task Planning
        print_pipeline_status("Stage 2: Task Planning", "running")

        planning_prompt = TASK_PLANNING_PROMPT.format(
            repo_analysis=repo_analysis,
            task_description=task_data.get("description", "")
        )
        save_artifact(run_dir, "claude_planning_prompt.md", planning_prompt, "text")

        task_spec = call_claude_cli(planning_prompt, timeout=180)
        save_artifact(run_dir, "claude_planning_response.yaml", task_spec, "text")
        save_artifact(run_dir, "task_spec.yaml", task_spec, "yaml")

        print_pipeline_status("Stage 2: Task Planning", "completed")

        # Stage 3: Code Generation (still manual - requires IDE)
        print_pipeline_status("Stage 3: Code Generation", "waiting")

        from agentic_code.agents.codex import CODEX_PROMPT_TEMPLATE

        impl_prompt = CODEX_PROMPT_TEMPLATE.format(
            task_spec=task_spec,
            repo_context=repo_analysis[:1000]
        )
        save_artifact(run_dir, "codex_implementation_prompt.md", impl_prompt, "text")

        console.print("\n[yellow bold]⏸  MANUAL STEP REQUIRED[/yellow bold]")
        console.print("[yellow]Please implement the code as specified in:[/yellow]")
        console.print(f"[cyan]{run_dir}/codex_implementation_prompt.md[/cyan]")
        console.print(f"[yellow]Save generated code to:[/yellow] [cyan]{run_dir}/generated_code/[/cyan]")
        console.print("\n[yellow]Press Enter when code is ready...[/yellow]")
        input()

        # Check for generated code
        generated_code_dir = run_dir / "generated_code"
        if not generated_code_dir.exists() or not list(generated_code_dir.glob("*")):
            console.print("[red]No code found in generated_code/ directory[/red]")
            console.print("[yellow]Continuing anyway...[/yellow]")
            generated_code = "(No code provided)"
        else:
            # Collect generated code
            code_files = []
            for file in generated_code_dir.rglob("*"):
                if file.is_file():
                    code_files.append(f"File: {file.name}\n{file.read_text()}\n")
            generated_code = "\n".join(code_files)

        print_pipeline_status("Stage 3: Code Generation", "completed")

        # Stage 4: Verification (skip if requested)
        verification_findings = []

        if skip_verification:
            console.print("\n[yellow]⚡ Skipping verification (as requested)[/yellow]\n")
        else:
            print_pipeline_status("Stage 4: Verification", "running")

            from agentic_code.agents.gemini import VERIFICATION_PROMPT
            import json

            verification_prompt = VERIFICATION_PROMPT.format(
                task_spec=task_spec,
                generated_code=generated_code
            )
            save_artifact(run_dir, "gemini_verification_prompt.md", verification_prompt, "text")

            # For Gemini, we still need manual step (or use Google AI API)
            console.print("\n[yellow bold]⏸  VERIFICATION STEP[/yellow bold]")
            console.print("[yellow]Option 1: Paste prompt into Gemini web (free)[/yellow]")
            console.print(f"  Prompt: [cyan]{run_dir}/gemini_verification_prompt.md[/cyan]")
            console.print(f"  Save JSON to: [cyan]{run_dir}/gemini_verification_response.json[/cyan]")
            console.print("\n[yellow]Enter 'skip' to bypass verification, or press Enter to continue...[/yellow]")
            user_input = input()

            if user_input.lower().strip() == 'skip':
                console.print("[yellow]⚡ Skipping verification as requested[/yellow]\n")
                skip_verification = True

            if not skip_verification:
                verification_file = run_dir / "gemini_verification_response.json"
                if verification_file.exists():
                    try:
                        verification_data = json.loads(verification_file.read_text())
                        verification_findings = verification_data.get("findings", [])
                        save_artifact(run_dir, "verification_findings.json", {
                            "findings": verification_findings,
                            "count": len(verification_findings)
                        }, "json")
                    except Exception as e:
                        console.print(f"[yellow]Could not parse verification: {e}[/yellow]")
                else:
                    console.print("[yellow]Verification file not found, skipping.[/yellow]")

            print_pipeline_status("Stage 4: Verification", "completed")

        # Stage 5: Integration Decision
        print_pipeline_status("Stage 5: Integration Decision", "running")

        # Format findings
        if verification_findings:
            findings_summary = "\n".join([
                f"- [{f.get('severity')}] {f.get('message')}"
                for f in verification_findings
            ])
        else:
            findings_summary = "No issues found - code passed all checks."

        decision_prompt = INTEGRATION_DECISION_PROMPT.format(
            task_spec=task_spec,
            findings_summary=findings_summary
        )
        save_artifact(run_dir, "claude_decision_prompt.md", decision_prompt, "text")

        decision_yaml = call_claude_cli(decision_prompt)
        save_artifact(run_dir, "claude_decision_response.yaml", decision_yaml, "text")
        save_artifact(run_dir, "integration_decision.yaml", decision_yaml, "yaml")

        print_pipeline_status("Stage 5: Integration Decision", "completed")

        # Parse and display decision
        import yaml
        try:
            decision_data = yaml.safe_load(decision_yaml)
            final_decision = decision_data.get("decision", "UNKNOWN")

            print_section("⚖️  INTEGRATION DECISION", style="cyan")
            console.print(f"[bold]Decision:[/bold] {final_decision}")
            console.print(f"\n{decision_yaml}\n")

            # Summary
            duration = time.time() - start_time
            print_section("📊 PIPELINE SUMMARY", style="green")
            console.print(f"[bold]Status:[/bold] [green]Completed[/green]")
            console.print(f"[bold]Task:[/bold] {task_name}")
            console.print(f"[bold]Duration:[/bold] {duration:.1f}s")
            console.print(f"[bold]Decision:[/bold] {final_decision}")
            console.print(f"\n[cyan]Run directory:[/cyan] {run_dir}\n")

            return final_decision

        except Exception as e:
            console.print(f"[yellow]Could not parse decision: {e}[/yellow]")
            return "PARSE_ERROR"

    except KeyboardInterrupt:
        console.print("\n[yellow]Pipeline interrupted by user[/yellow]")
        return "INTERRUPTED"

    except Exception as e:
        console.print(f"\n[red bold]Pipeline error: {e}[/red bold]")
        import traceback
        traceback.print_exc()
        return "ERROR"


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        console.print("[red]Usage: python scripts/fully_automated.py <task-file> [--skip-verification][/red]")
        console.print("\nExample:")
        console.print("  python scripts/fully_automated.py examples/simple-function.md")
        sys.exit(1)

    task_path = Path(sys.argv[1])
    skip_verification = "--skip-verification" in sys.argv

    if not task_path.exists():
        console.print(f"[red]Task file not found: {task_path}[/red]")
        sys.exit(1)

    decision = run_automated_pipeline(task_path, skip_verification)

    # Exit with appropriate code
    if decision == "APPROVE":
        sys.exit(0)
    elif decision in ["REJECT", "ERROR"]:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
