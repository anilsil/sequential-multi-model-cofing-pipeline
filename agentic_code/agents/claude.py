"""
Claude Agent - Architect, Planner, and Integrator (Prompt-Based and Automated).

This agent generates prompts for Claude Code CLI or calls the API.

Responsibilities:
- Generate prompts for repository analysis
- Generate prompts for task planning
- Generate prompts for integration decisions
- Wait for user to paste responses (prompt-based mode)
- Execute prompts via API (automated mode)
"""

from pathlib import Path
from typing import Dict, Any
import yaml
import os
import anthropic
from ..config import Config
from ..utils import console, save_artifact, confirm_action, print_section


# Prompt templates for Claude
REPO_ANALYSIS_PROMPT = """# Repository Analysis Task

You are analyzing a codebase to understand its structure and patterns.

## Repository Information
- Location: {repo_root}
- Purpose: Understand existing patterns before implementing new features

## Your Task
Analyze this repository and provide:

1. **Primary Language(s)**: What languages are primarily used?
2. **Project Type**: Web app, CLI tool, library, etc.
3. **Key Frameworks**: What major frameworks/libraries are in use?
4. **Code Organization**: How is the code structured? (src/, lib/, app/, etc.)
5. **Testing Approach**: What testing framework is used? Where are tests located?
6. **Notable Patterns**: Any architectural patterns (MVC, microservices, etc.)?
7. **Dependencies**: Key dependencies from package files
8. **Code Style**: Naming conventions, formatting preferences

## Output Format
Provide a concise analysis (200-300 words) focusing on facts that would help implement new features consistently with existing patterns.

**Begin your analysis:**
"""

TASK_PLANNING_PROMPT = """# Task Planning - Create Implementation Specification

You are a software architect creating a detailed implementation plan.

## Context
{repo_analysis}

## Task Description
{task_description}

## Your Job
Create a YAML specification that a developer can follow to implement this task.

## Required YAML Structure
```yaml
task_name: brief-descriptive-name
objective: One sentence describing the goal
requirements:
  - Specific requirement 1
  - Specific requirement 2
  - ...
files_to_modify:
  - path/to/file1.ext
  - path/to/file2.ext
new_files:
  - path/to/new_file1.ext
implementation_steps:
  - Step 1: Description
  - Step 2: Description
  - ...
testing_requirements:
  - Test requirement 1
  - Test requirement 2
constraints:
  - Do NOT modify X
  - Follow pattern Y
  - ...
```

## Critical Guidelines
- Be SPECIFIC about file paths and locations
- Follow existing repository patterns (from analysis above)
- Minimize scope - only what's truly necessary
- No new dependencies unless absolutely critical
- Consider backward compatibility
- Include comprehensive testing requirements

**Output ONLY the YAML specification (no markdown code blocks, no explanations):**
"""

INTEGRATION_DECISION_PROMPT = """# Integration Decision - Review and Approve/Reject

You are making the final decision on whether to integrate generated code.

## Original Task Specification
```yaml
{task_spec}
```

## Verification Findings
{findings_summary}

## Your Decision
Review the verification findings and decide:

1. **APPROVE** - Code meets quality standards, safe to integrate
2. **REJECT** - Critical issues found, must fix before integration
3. **APPROVE_WITH_NOTES** - Minor issues, can integrate with documented caveats

## Required Output Format (YAML)
```yaml
decision: APPROVE | REJECT | APPROVE_WITH_NOTES
rationale: |
  Clear explanation of why you made this decision.
  Reference specific findings.
  Explain risk assessment.

required_fixes:  # Only if REJECT
  - Fix 1
  - Fix 2

recommended_improvements:  # Optional enhancements
  - Improvement 1
  - Improvement 2

integration_notes:  # Important caveats or follow-up items
  - Note 1
  - Note 2
```

## Decision Criteria
- **HIGH severity issues** → Likely REJECT
- **Multiple MEDIUM issues** → Carefully evaluate
- **Only LOW issues** → Likely APPROVE or APPROVE_WITH_NOTES
- **Security vulnerabilities** → Always REJECT until fixed
- **Logic errors** → REJECT
- **Style/minor issues** → APPROVE_WITH_NOTES

**Output ONLY the YAML decision (no markdown code blocks, no explanations):**
"""


class ClaudeAgent:
    """
    Claude agent for planning and integration (prompt-based and automated).
    """

    def __init__(self, config: Config, automated: bool = False):
        """Initialize Claude agent."""
        self.config = config
        self.automated = automated
        if self.automated:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable not set")
            self.client = anthropic.Anthropic(api_key=api_key)

    def _execute_prompt(self, prompt: str) -> str:
        """Execute a prompt using the Claude API."""
        if not self.automated:
            raise RuntimeError("_execute_prompt can only be called in automated mode")
        
        if self.config.test_mode:
            console.print("[dim]Simulating Claude API response in test mode...[/dim]")
            if "REPO_ANALYSIS_PROMPT" in prompt:
                return "Simulated repository analysis."
            elif "TASK_PLANNING_PROMPT" in prompt:
                return """
task_name: simulated-task
objective: Simulate a task planning process
requirements:
  - Implement a dummy function
files_to_modify: []
new_files:
  - src/simulated_module.py
implementation_steps:
  - Create the file src/simulated_module.py
  - Add a dummy function
testing_requirements:
  - Add a unit test for the dummy function
constraints: []
"""
            elif "INTEGRATION_DECISION_PROMPT" in prompt:
                return """
decision: APPROVE
rationale: |
  Simulated approval in test mode.
"""
            return "Simulated Claude response in test mode."

        console.print("[blue]🤖 Claude: Executing prompt via API...[/blue]")
        message = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2048,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text

    def execute_analysis(self, repo_root: Path) -> str:
        """Execute repository analysis."""
        prompt = REPO_ANALYSIS_PROMPT.format(repo_root=repo_root)
        return self._execute_prompt(prompt)

    def execute_planning(self, task_description: str, repo_analysis: str) -> str:
        """Execute task planning."""
        prompt = TASK_PLANNING_PROMPT.format(
            repo_analysis=repo_analysis,
            task_description=task_description
        )
        return self._execute_prompt(prompt)

    def execute_decision(self, task_spec: str, verification_findings: list[Dict[str, Any]]) -> str:
        """Execute integration decision."""
        findings_summary = self._format_findings(verification_findings)
        prompt = INTEGRATION_DECISION_PROMPT.format(
            task_spec=task_spec,
            findings_summary=findings_summary
        )
        return self._execute_prompt(prompt)

    def generate_analysis_prompt(self, repo_root: Path, run_dir: Path) -> Path:
        """
        Generate prompt for repository analysis.
        """
        console.print("[blue]📝 Claude: Generating repository analysis prompt...[/blue]")

        prompt = REPO_ANALYSIS_PROMPT.format(repo_root=repo_root)

        prompt_file = save_artifact(run_dir, "claude_analysis_prompt.md", prompt, "text")

        console.print(f"\n[cyan bold]→ Prompt generated: {prompt_file}[/cyan bold]")
        return prompt_file

    def generate_planning_prompt(
        self,
        task_description: str,
        repo_analysis: str,
        run_dir: Path
    ) -> Path:
        """
        Generate prompt for task planning.
        """
        console.print("[blue]📝 Claude: Generating task planning prompt...[/blue]")

        prompt = TASK_PLANNING_PROMPT.format(
            repo_analysis=repo_analysis,
            task_description=task_description
        )

        prompt_file = save_artifact(run_dir, "claude_planning_prompt.md", prompt, "text")

        console.print(f"\n[cyan bold]→ Prompt generated: {prompt_file}[/cyan bold]")
        return prompt_file

    def generate_decision_prompt(
        self,
        task_spec: str,
        verification_findings: list[Dict[str, Any]],
        run_dir: Path
    ) -> Path:
        """
        Generate prompt for integration decision.
        """
        console.print("[blue]📝 Claude: Generating integration decision prompt...[/blue]")

        findings_summary = self._format_findings(verification_findings)

        prompt = INTEGRATION_DECISION_PROMPT.format(
            task_spec=task_spec,
            findings_summary=findings_summary
        )

        prompt_file = save_artifact(run_dir, "claude_decision_prompt.md", prompt, "text")

        console.print(f"\n[cyan bold]→ Prompt generated: {prompt_file}[/cyan bold]")
        return prompt_file

    def wait_for_response(self, prompt_file: Path, response_file: Path, stage_name: str) -> str:
        """
        Wait for user to provide Claude's response.
        """
        print_section(f"⏸  HUMAN ACTION REQUIRED: {stage_name}", style="yellow")

        console.print(f"[yellow bold]STEPS:[/yellow bold]\n")
        console.print(f"1. Open Claude Code CLI (the tool you're using right now)")
        console.print(f"2. Paste the contents of: [cyan]{prompt_file}[/cyan]")
        console.print(f"3. Copy Claude's response")
        console.print(f"4. Save it to: [cyan]{response_file}[/cyan]")
        console.print(f"5. Return here and confirm\n")

        ready = confirm_action(
            f"Have you saved Claude's response to {response_file.name}?",
            default=False
        )

        if not ready:
            raise KeyboardInterrupt("User cancelled")

        if not response_file.exists():
            console.print(f"[red]Error: Response file not found: {response_file}[/red]")
            retry = confirm_action("Try again?", default=True)
            if retry:
                return self.wait_for_response(prompt_file, response_file, stage_name)
            raise FileNotFoundError(f"Response file not found: {response_file}")

        response = response_file.read_text()

        if not response.strip():
            console.print("[red]Error: Response file is empty[/red]")
            retry = confirm_action("Try again?", default=True)
            if retry:
                return self.wait_for_response(prompt_file, response_file, stage_name)
            raise ValueError("Response file is empty")

        console.print(f"[green]✓ Response loaded ({len(response)} characters)[/green]\n")
        return response

    def _format_findings(self, findings: list[Dict[str, Any]]) -> str:
        """Format verification findings for prompt."""
        if not findings:
            return "No issues found - code passed all verification checks."

        high = [f for f in findings if f.get("severity") == "HIGH"]
        medium = [f for f in findings if f.get("severity") == "MEDIUM"]
        low = [f for f in findings if f.get("severity") == "LOW"]

        summary = f"""
**Summary:**
- HIGH severity: {len(high)}
- MEDIUM severity: {len(medium)}
- LOW severity: {len(low)}
- Total: {len(findings)}

**Detailed Findings:**
"""
        for i, finding in enumerate(findings, 1):
            summary += f"\n{i}. [{finding.get('severity')}] {finding.get('category', 'General')}\n"
            summary += f"   Issue: {finding.get('message')}\n"
            summary += f"   Location: {finding.get('location', 'Unknown')}\n"
            summary += f"   Suggestion: {finding.get('suggestion', 'None')}\n"

        return summary
