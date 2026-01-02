"""
Codex Agent - Implementation Agent (Human-in-the-Loop and Automated).

Responsibilities:
- Generate code based on task specification
- Follow repository patterns and conventions
- Create tests alongside implementation
- MUST be human-supervised (no auto-commit)

This adapter creates prompts for Cursor/Codex or calls the Gemini API.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import time
import os
import re
import subprocess
import google.generativeai as genai
from ..config import Config
from ..utils import console, save_artifact, confirm_action, print_section


# Updated prompt template for automated generation
CODEX_PROMPT_TEMPLATE = """# Implementation Task

You are an implementation agent. Your ONLY job is to write clean, working code based on the specification.

## STRICT RULES:
1. Follow the task specification EXACTLY.
2. Follow existing repository patterns.
3. NO new dependencies unless specified.
4. Add tests for all new functionality.
5. Output code in the specified format ONLY.
6. DO NOT write any explanations or conversational text.

## TASK SPECIFICATION:
{task_spec}

## REPOSITORY CONTEXT:
{repo_context}

## OUTPUT REQUIREMENTS:
You MUST output the code for each file using the following format. Do not add any other text or explanations.

-- FILE: path/to/your/file.py --
```python
# Your code here
```
-- ENDFILE --

-- FILE: path/to/your/test_file.py --
```python
# Your test code here
```
-- ENDFILE --

-- FILE: summary.md --
```markdown
### Implementation Summary
- **Files Created**: `path/to/your/file.py`, `path/to/your/test_file.py`
- **Key Decisions**: Brief explanation of any choices made.
- **How to Run**: Instructions on how to run or test the new code.
```
-- ENDFILE --

BEGIN IMPLEMENTATION NOW.
"""


class CodexAgent:
    """
    Codex agent adapter for code generation (human-in-the-loop and automated).
    """

    def __init__(self, config: Config, automated: bool = False):
        """
        Initialize Codex agent.
        """
        self.config = config
        self.automated = automated
        if self.automated:
            if not self.config.implementation_cli_command:
                api_key = os.getenv("GEMINI_API_KEY")
                if not api_key:
                    raise ValueError("GEMINI_API_KEY environment variable not set and implementation_cli_command is not configured")
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-pro')

    def _execute_cli_implementation(self, prompt: str) -> str:
        """Execute implementation using a configured CLI command."""
        console.print(f"[green]🤖 Codex: Executing implementation via CLI: {self.config.implementation_cli_command}[/green]")
        try:
            result = subprocess.run(
                self.config.implementation_cli_command,
                input=prompt,
                capture_output=True,
                text=True,
                timeout=300, # 5-minute timeout for code generation
                check=True,
                shell=True # Use shell=True to handle complex commands
            )
            return result.stdout.strip()
        except FileNotFoundError:
            raise RuntimeError(f"The command '{self.config.implementation_cli_command}' was not found.")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"The command failed with exit code {e.returncode}. Stderr: {e.stderr}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("The implementation command timed out.")

    def execute_implementation(self, task_spec: str, repo_context: str, run_dir: Path) -> Dict[str, Any]:
        """
        Execute implementation using Gemini API and save the generated files.
        """
        if not self.automated:
            raise RuntimeError("execute_implementation can only be called in automated mode")

        if self.config.test_mode:
            console.print("[dim]Simulating Codex API response and file creation in test mode...[/dim]")
            output_dir = run_dir / "generated_code"
            output_dir.mkdir(exist_ok=True)
            
            # Simulate a generated file
            dummy_file_path = output_dir / "src/dummy_module.py"
            dummy_file_path.parent.mkdir(parents=True, exist_ok=True)
            dummy_file_path.write_text("def dummy_function():\n    return 'Hello from dummy!'")
            
            summary_file_path = output_dir / "summary.md"
            summary_file_path.write_text("### Implementation Summary\n- Files Created: `src/dummy_module.py`\n- Key Decisions: Simulated decision.\n- How to Run: N/A")

            return {
                "status": "completed",
                "file_count": 2,
                "files": ["src/dummy_module.py", "summary.md"]
            }

        output_dir = run_dir / "generated_code"
        output_dir.mkdir(exist_ok=True)

        prompt = CODEX_PROMPT_TEMPLATE.format(
            task_spec=task_spec,
            repo_context=repo_context,
            output_dir=output_dir
        )

        if self.config.implementation_cli_command:
            response_text = self._execute_cli_implementation(prompt)
        else:
            console.print("[green]🤖 Codex (via Gemini): Executing implementation...")
            response_text = self.model.generate_content(prompt).text
        
        # Save raw response for debugging
        save_artifact(run_dir, "codex_raw_response.md", response_text, "text")

        files = self._parse_and_save_files(response_text, output_dir)

        if not files:
            console.print("[red]⚠ No files were generated or parsed from the response.[/red]")
            return {"status": "no_files", "file_count": 0, "files": []}

        console.print(f"\n[green]✓ Generated {len(files)} files:[/green]")
        for file in files:
            console.print(f"  - {file}")

        return {
            "status": "completed",
            "file_count": len(files),
            "files": files
        }

    def _parse_and_save_files(self, response_text: str, output_dir: Path) -> list[str]:
        """Parse the model's response and save the files."""
        file_pattern = re.compile(r"-- FILE: (.*?) --\n```(?:\w+\n)?(.*?)\n```\n-- ENDFILE --", re.DOTALL)
        matches = file_pattern.findall(response_text)
        
        saved_files = []
        for file_path_str, content in matches:
            file_path = output_dir / file_path_str.strip()
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content.strip())
            saved_files.append(file_path_str.strip())
            
        return saved_files

    def generate_implementation_prompt(
        self,
        task_spec: str,
        repo_context: str,
        run_dir: Path
    ) -> Path:
        """
        Generate a prompt file for the human-in-the-loop workflow.
        """
        console.print("[green]🤖 Codex: Generating implementation prompt...[/green]")

        output_dir = run_dir / "generated_code"
        output_dir.mkdir(exist_ok=True)

        prompt = CODEX_PROMPT_TEMPLATE.format(
            task_spec=task_spec,
            repo_context=repo_context,
            output_dir=output_dir
        ).replace("-- FILE:", "## FILE:").replace("-- ENDFILE --", "### ENDFILE")


        prompt_file = save_artifact(run_dir, "codex_implementation_prompt.md", prompt, "text")

        console.print(f"\n[green bold]✓ Implementation prompt generated![/green bold]")
        console.print(f"[dim]Location: {prompt_file}[/dim]\n")

        return prompt_file

    def wait_for_implementation(self, run_dir: Path) -> Dict[str, Any]:
        """
        Pause execution and wait for user to complete implementation.
        """
        print_section("⏸  HUMAN-IN-THE-LOOP PAUSE", style="yellow")

        console.print("[yellow bold]ACTION REQUIRED:[/yellow bold]")
        console.print("\n1. Open the codex_implementation_prompt.md file in your AI-enabled IDE")
        console.print("2. Use your AI assistant to implement the specification")
        console.print("3. Review the generated code carefully")
        console.print("4. Save all generated files to the generated_code/ directory")
        console.print("5. Return here when complete\n")

        prompt_file = run_dir / "codex_implementation_prompt.md"
        output_dir = run_dir / "generated_code"

        console.print(f"[cyan]Prompt file:[/cyan] {prompt_file}")
        console.print(f"[cyan]Output directory:[/cyan] {output_dir}\n")

        if self.config.batch_mode:
            console.print("[yellow]Batch mode: Skipping human confirmation[/yellow]")
            return {"status": "skipped", "mode": "batch"}

        ready = confirm_action(
            "Have you completed the implementation and saved files to generated_code/?",
            default=False
        )

        if not ready:
            console.print("[red]Implementation cancelled by user.[/red]")
            return {"status": "cancelled"}

        generated_files = list(output_dir.rglob("*"))
        generated_files = [f for f in generated_files if f.is_file()]

        if not generated_files:
            console.print("[red]⚠ No files found in generated_code/ directory![/red]")
            retry = confirm_action("Continue anyway?", default=False)
            if not retry:
                return {"status": "no_files"}

        console.print(f"\n[green]✓ Found {len(generated_files)} generated files:[/green]")
        for file in generated_files[:10]:
            console.print(f"  - {file.relative_to(output_dir)}")
        if len(generated_files) > 10:
            console.print(f"  ... and {len(generated_files) - 10} more")

        return {
            "status": "completed",
            "file_count": len(generated_files),
            "files": [str(f.relative_to(output_dir)) for f in generated_files]
        }

    def collect_generated_code(self, run_dir: Path) -> Optional[str]:
        """
        Collect all generated code into a single string for verification.
        """
        output_dir = run_dir / "generated_code"

        if not output_dir.exists():
            return None

        code_parts = []
        generated_files = sorted(output_dir.rglob("*"))

        for file_path in generated_files:
            if not file_path.is_file():
                continue

            skip_extensions = {'.pyc', '.pyo', '.so', '.dylib', '.exe', '.jpg', '.png', '.gif'}
            if file_path.suffix in skip_extensions:
                continue

            try:
                relative_path = file_path.relative_to(output_dir)
                content = file_path.read_text()
                code_parts.append(f"# File: {relative_path}\n{content}\n\n")
            except (UnicodeDecodeError, PermissionError):
                continue

        return "\n".join(code_parts) if code_parts else None
