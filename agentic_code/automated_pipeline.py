"""
Automated pipeline orchestration for agentic-code.

Coordinates a sequential multi-model workflow using API calls with human-in-the-loop
governance. This is a sequential pipeline with separation of duties, not a concurrent
multi-agent system.
"""

import time
from pathlib import Path
from typing import Dict, Any
import yaml

from .config import Config
from .agents import ClaudeAgent, CodexAgent, GeminiAgent
from .utils import (
    console,
    create_run_directory,
    load_task_file,
    print_section,
    print_artifact_summary,
    print_pipeline_status,
    format_duration,
    confirm_action,
)


class AutomatedAgenticPipeline:
    """
    Orchestrates the governed multi-model sequential pipeline (automated).

    Sequential multi-model architecture with API automation and human governance.
    """

    def __init__(self, config: Config):
        """Initialize pipeline with configuration."""
        self.config = config
        self.claude = ClaudeAgent(config, automated=True)
        self.codex = CodexAgent(config, automated=True)
        self.gemini = GeminiAgent(config, automated=True)

    def run(self, task_path: Path) -> Dict[str, Any]:
        """
        Run the complete agentic pipeline (automated).

        Pipeline stages:
        1. Load task specification
        2. Generate repository analysis (Claude)
        3. Generate task planning (Claude)
        4. Generate code (Codex)
        5. Verify code (Gemini) [optional]
        6. Decide on integration (Claude)

        Args:
            task_path: Path to task specification file

        Returns:
            Pipeline execution results
        """
        start_time = time.time()

        print_section("🚀 AGENTIC CODE PIPELINE (Automated)", style="blue")
        console.print(f"[dim]Task: {task_path}[/dim]")
        console.print(f"[dim]Mode: Fully Automated with Human Review[/dim]\n")

        # Load task
        task_data = load_task_file(task_path)
        task_name = task_data.get("name", task_path.stem)

        # Create run directory
        run_dir = create_run_directory(self.config.output_dir, task_name)
        console.print(f"[cyan]Run directory:[/cyan] {run_dir}\n")

        results = {
            "task_name": task_name,
            "run_dir": str(run_dir),
            "start_time": start_time,
            "stages": {}
        }

        try:
            # Stage 1: Repository Analysis (Claude)
            print_pipeline_status("Stage 1: Repository Analysis (Claude)", "running")
            repo_analysis = self.claude.execute_analysis(self.config.repo_root)
            print_section("Claude's Analysis", style="blue")
            console.print(repo_analysis)
            if not confirm_action("Proceed with planning?", test_mode=self.config.test_mode):
                results["status"] = "cancelled_at_planning"
                return results
            results["stages"]["analysis"] = {"status": "completed", "response_length": len(repo_analysis)}
            print_pipeline_status("Stage 1: Repository Analysis (Claude)", "completed")

            # Stage 2: Task Planning (Claude)
            print_pipeline_status("Stage 2: Task Planning (Claude)", "running")
            task_spec_yaml = self.claude.execute_planning(task_data.get("description", ""), repo_analysis)
            print_section("Claude's Plan", style="blue")
            console.print(task_spec_yaml)
            if not confirm_action("Proceed with implementation?", test_mode=self.config.test_mode):
                results["status"] = "cancelled_at_implementation"
                return results
            results["stages"]["planning"] = {"status": "completed", "spec_length": len(task_spec_yaml)}
            print_pipeline_status("Stage 2: Task Planning (Claude)", "completed")

            # Stage 3: Code Generation (Codex/Gemini)
            print_pipeline_status("Stage 3: Code Generation (Codex/Gemini)", "running")
            impl_result = self.codex.execute_implementation(task_spec_yaml, repo_analysis[:1000], run_dir)
            results["stages"]["implementation"] = impl_result
            if not confirm_action("Proceed with verification?", test_mode=self.config.test_mode):
                results["status"] = "cancelled_at_verification"
                return results
            print_pipeline_status("Stage 3: Code Generation (Codex/Gemini)", "completed")

            # Collect generated code
            generated_code = self.codex.collect_generated_code(run_dir)

            # Stage 4: Verification (Gemini) [Optional]
            if self.config.skip_verification:
                console.print("\n[yellow]⚡ Skipping verification (as requested)[/yellow]\n")
                verification_findings = []
                results["stages"]["verification"] = {"status": "skipped"}
            else:
                print_pipeline_status("Stage 4: Verification (Gemini)", "running")
                verification_prompt = self.gemini.generate_verification_prompt(
                    task_spec=task_spec_yaml,
                    generated_code=generated_code or "(no code collected)",
                    run_dir=run_dir
                )
                verification_result_text = self.gemini.execute_verification(verification_prompt.read_text())
                verification_findings = self.gemini._parse_findings(verification_result_text)
                self.gemini._print_verification_summary(verification_findings)
                if not confirm_action("Proceed with final decision?", test_mode=self.config.test_mode):
                    results["status"] = "cancelled_at_decision"
                    return results
                results["stages"]["verification"] = {"status": "completed", "findings": verification_findings}
                print_pipeline_status("Stage 4: Verification (Gemini)", "completed")

            # Stage 5: Integration Decision (Claude)
            print_pipeline_status("Stage 5: Integration Decision (Claude)", "running")
            decision_yaml = self.claude.execute_decision(task_spec_yaml, verification_findings)
            print_section("Claude's Decision", style="blue")
            console.print(decision_yaml)
            results["stages"]["decision"] = {"status": "completed"}
            print_pipeline_status("Stage 5: Integration Decision (Claude)", "completed")
            
            # Parse decision
            try:
                decision_data = yaml.safe_load(decision_yaml)
                final_decision = decision_data.get("decision", "UNKNOWN")
                results["final_decision"] = final_decision
            except Exception as e:
                console.print(f"[yellow]⚠ Could not parse decision: {e}[/yellow]")
                results["final_decision"] = "PARSE_ERROR"


            # Mark as completed
            results["status"] = "completed"
            results["end_time"] = time.time()
            results["duration"] = results["end_time"] - start_time

        except KeyboardInterrupt:
            console.print("\n\n[red]Pipeline interrupted by user[/red]")
            results["status"] = "interrupted"
            results["end_time"] = time.time()

        except Exception as e:
            console.print(f"\n\n[red bold]Pipeline error: {e}[/red bold]")
            import traceback
            traceback.print_exc()
            results["status"] = "error"
            results["error"] = str(e)
            results["end_time"] = time.time()

        # Print summary
        self._print_summary(results)

        return results

    def _print_summary(self, results: Dict[str, Any]) -> None:
        """Print pipeline execution summary."""
        print_section("📊 PIPELINE SUMMARY", style="green")

        status = results.get("status", "unknown")
        status_color = {
            "completed": "green",
            "interrupted": "yellow",
            "error": "red",
        }.get(status, "white")

        console.print(f"[bold]Status:[/bold] [{status_color}]{status}[/{status_color}]")
        console.print(f"[bold]Task:[/bold] {results.get('task_name', 'Unknown')}")

        if "duration" in results:
            console.print(f"[bold]Duration:[/bold] {format_duration(results['duration'])}")

        if "final_decision" in results:
            decision = results["final_decision"]
            decision_color = {
                "APPROVE": "green",
                "REJECT": "red",
                "APPROVE_WITH_NOTES": "yellow"
            }.get(decision, "white")
            console.print(f"[bold]Decision:[/bold] [{decision_color}]{decision}[/{decision_color}]")

        # Print artifact summary
        run_dir = Path(results.get("run_dir", "output"))
        if run_dir.exists():
            print_artifact_summary(run_dir)