"""
Pipeline orchestration for agentic-code (Prompt-Based).

Coordinates the multi-agent workflow using prompt generation and human-in-the-loop:
1. Claude analyzes (prompt → user pastes response)
2. Claude plans (prompt → user pastes response)
3. Codex implements (prompt → user implements)
4. Gemini verifies (prompt → user pastes response) [OPTIONAL]
5. Claude decides (prompt → user pastes response)

All steps are human-supervised. Zero API costs!
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
)


class AgenticPipeline:
    """
    Orchestrates the governed multi-agent coding pipeline (prompt-based).

    100% free - generates prompts for user to paste into AI tools.
    """

    def __init__(self, config: Config):
        """Initialize pipeline with configuration."""
        self.config = config
        self.claude = ClaudeAgent(config)
        self.codex = CodexAgent(config)
        self.gemini = GeminiAgent(config)

    def run(self, task_path: Path) -> Dict[str, Any]:
        """
        Run the complete agentic pipeline (prompt-based).

        Pipeline stages:
        1. Load task specification
        2. Generate repository analysis prompt (Claude)
        3. Generate task planning prompt (Claude)
        4. Generate code (Codex + Human)
        5. Generate verification prompt (Gemini) [optional]
        6. Generate integration decision prompt (Claude)

        Args:
            task_path: Path to task specification file

        Returns:
            Pipeline execution results
        """
        start_time = time.time()

        print_section("🚀 AGENTIC CODE PIPELINE (Prompt Orchestrator)", style="blue")
        console.print(f"[dim]Task: {task_path}[/dim]")
        console.print(f"[dim]Mode: 100% Free - Human-in-the-loop prompts[/dim]\n")

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

            analysis_prompt_file = self.claude.generate_analysis_prompt(
                self.config.repo_root,
                run_dir
            )

            analysis_response_file = run_dir / "claude_analysis_response.txt"
            repo_analysis = self.claude.wait_for_response(
                analysis_prompt_file,
                analysis_response_file,
                "Repository Analysis"
            )

            results["stages"]["analysis"] = {
                "status": "completed",
                "response_length": len(repo_analysis)
            }
            print_pipeline_status("Stage 1: Repository Analysis (Claude)", "completed")

            # Stage 2: Task Planning (Claude)
            print_pipeline_status("Stage 2: Task Planning (Claude)", "running")

            planning_prompt_file = self.claude.generate_planning_prompt(
                task_description=task_data.get("description", ""),
                repo_analysis=repo_analysis,
                run_dir=run_dir
            )

            planning_response_file = run_dir / "claude_planning_response.yaml"
            task_spec = self.claude.wait_for_response(
                planning_prompt_file,
                planning_response_file,
                "Task Planning"
            )

            # Save task spec
            from .utils import save_artifact
            save_artifact(run_dir, "task_spec.yaml", task_spec, "yaml")

            results["stages"]["planning"] = {
                "status": "completed",
                "spec_length": len(task_spec)
            }
            print_pipeline_status("Stage 2: Task Planning (Claude)", "completed")

            # Stage 3: Code Generation (Codex + Human)
            print_pipeline_status("Stage 3: Code Generation (Codex + Human)", "running")

            codex_prompt_file = self.codex.generate_implementation_prompt(
                task_spec=task_spec,
                repo_context=repo_analysis[:1000],  # Brief context
                run_dir=run_dir
            )

            impl_result = self.codex.wait_for_implementation(run_dir)
            results["stages"]["implementation"] = impl_result

            if impl_result.get("status") in ["cancelled", "no_files"]:
                results["status"] = f"cancelled_at_implementation"
                return results

            print_pipeline_status("Stage 3: Code Generation (Codex + Human)", "completed")

            # Collect generated code
            generated_code = self.codex.collect_generated_code(run_dir)

            # Stage 4: Verification (Gemini) [Optional]
            if self.config.skip_verification:
                console.print("\n[yellow]⚡ Skipping verification (as requested)[/yellow]\n")
                verification_findings = []
                results["stages"]["verification"] = {"status": "skipped"}
            else:
                print_pipeline_status("Stage 4: Verification (Gemini)", "running")

                verification_prompt_file = self.gemini.generate_verification_prompt(
                    task_spec=task_spec,
                    generated_code=generated_code or "(no code collected)",
                    run_dir=run_dir
                )

                verification_response_file = run_dir / "gemini_verification_response.json"
                verification_result = self.gemini.wait_for_verification(
                    verification_prompt_file,
                    verification_response_file
                )

                verification_findings = verification_result.get("findings", [])
                results["stages"]["verification"] = verification_result

                # Save findings
                save_artifact(run_dir, "verification_findings.json", {
                    "findings": verification_findings,
                    "count": len(verification_findings)
                }, "json")

                print_pipeline_status("Stage 4: Verification (Gemini)", "completed")

            # Stage 5: Integration Decision (Claude)
            print_pipeline_status("Stage 5: Integration Decision (Claude)", "running")

            decision_prompt_file = self.claude.generate_decision_prompt(
                task_spec=task_spec,
                verification_findings=verification_findings,
                run_dir=run_dir
            )

            decision_response_file = run_dir / "claude_decision_response.yaml"
            decision_yaml = self.claude.wait_for_response(
                decision_prompt_file,
                decision_response_file,
                "Integration Decision"
            )

            # Save decision
            save_artifact(run_dir, "integration_decision.yaml", decision_yaml, "yaml")

            print_pipeline_status("Stage 5: Integration Decision (Claude)", "completed")

            # Parse decision
            try:
                decision_data = yaml.safe_load(decision_yaml)
                final_decision = decision_data.get("decision", "UNKNOWN")
                results["final_decision"] = final_decision

                # Display decision
                print_section("⚖️  INTEGRATION DECISION", style="cyan")
                console.print(f"[bold]Decision:[/bold] {final_decision}")
                console.print(f"\n{decision_yaml}\n")

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
