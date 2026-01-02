"""
Gemini Agent - Verification Agent (Prompt-Based and Automated).

This agent generates prompts for Gemini (via web interface or API) - can be skipped!

Responsibilities:
- Generate prompts for code verification
- Wait for user to paste verification results (prompt-based mode)
- Execute verification via API (automated mode)
- Parse and structure findings
- MUST NOT generate code rewrites
"""

from pathlib import Path
from typing import Dict, Any, List
import json
import os
import google.generativeai as genai
from ..config import Config
from ..utils import console, save_artifact, confirm_action, print_section, print_findings


VERIFICATION_PROMPT = """# Code Verification Task

You are a code verification specialist. Your ONLY job is to find issues - NOT to fix them or rewrite code.

## Task Specification
```yaml
{task_spec}
```

## Code to Verify
```
{generated_code}
```

## Verification Checklist

### 1. Logical Correctness
- Does the code meet the task requirements?
- Are there logic errors or edge cases not handled?
- Are algorithms implemented correctly?
- Off-by-one errors?

### 2. Security Issues
- SQL injection vulnerabilities?
- XSS (Cross-Site Scripting) vulnerabilities?
- Insecure data handling?
- Authentication/authorization bypasses?
- Sensitive data exposure in logs?
- Unsafe deserialization?
- Path traversal vulnerabilities?

### 3. Concurrency & Race Conditions
- Thread safety issues?
- Resource locking problems?
- Race conditions in async code?
- Deadlock potential?

### 4. Error Handling
- Are exceptions properly caught?
- Are error messages informative (but not leaking sensitive info)?
- Are resources cleaned up in finally blocks?
- Are edge cases handled (null, empty, invalid input)?

### 5. Performance Risks
- N+1 query problems?
- Inefficient algorithms (O(n^2) where O(n) possible)?
- Memory leaks?
- Unnecessary database calls?
- Missing indices or caching?

## Output Format

Return a JSON array of findings. Each finding MUST have:
```json
[
  {{
    "severity": "HIGH" | "MEDIUM" | "LOW",
    "category": "Security" | "Logic" | "Concurrency" | "ErrorHandling" | "Performance",
    "message": "Clear description of the issue",
    "location": "File and line/function where issue occurs",
    "suggestion": "How to fix (plain language, NO CODE)"
  }}
]
```

**CRITICAL RULES:**
1. Output ONLY valid JSON (no markdown code blocks)
2. If no issues found, return empty array: `[]`
3. Do NOT include code snippets in suggestions
4. Do NOT rewrite or implement fixes
5. Focus on genuine issues, not style preferences

**Begin verification - output JSON only:**
"""


class GeminiAgent:
    """
    Gemini agent for code verification (prompt-based and automated).
    """

    def __init__(self, config: Config, automated: bool = False):
        """Initialize Gemini agent."""
        self.config = config
        self.automated = automated
        if self.automated:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY environment variable not set")
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')

    def generate_verification_prompt(
        self,
        task_spec: str,
        generated_code: str,
        run_dir: Path
    ) -> Path:
        """
        Generate prompt for code verification.
        """
        console.print("[magenta]📝 Gemini: Generating verification prompt...[/magenta]")

        max_code_length = 50000
        if len(generated_code) > max_code_length:
            console.print(f"[yellow]⚠ Code truncated to {max_code_length} chars[/yellow]")
            generated_code = generated_code[:max_code_length] + "\n\n... [TRUNCATED]"

        prompt = VERIFICATION_PROMPT.format(
            task_spec=task_spec,
            generated_code=generated_code
        )

        prompt_file = save_artifact(run_dir, "gemini_verification_prompt.md", prompt, "text")

        console.print(f"\n[magenta bold]→ Prompt generated: {prompt_file}[/magenta bold]")
        return prompt_file

    def execute_verification(self, prompt: str) -> str:
        """
        Execute verification using Gemini API.
        """
        if not self.automated:
            raise RuntimeError("execute_verification can only be called in automated mode")
        
        if self.config.test_mode:
            console.print("[dim]Simulating Gemini API response in test mode...[/dim]")
            return """
[
  {
    "severity": "LOW",
    "category": "Performance",
    "message": "Simulated finding: Function could be optimized.",
    "location": "src/main.py:10",
    "suggestion": "Consider alternative algorithm."
  }
]
"""

        console.print("[magenta]🤖 Gemini: Executing verification via API...[/magenta]")
        response = self.model.generate_content(prompt)
        return response.text

    def wait_for_verification(self, prompt_file: Path, response_file: Path) -> Dict[str, Any]:
        """
        Wait for user to provide Gemini's verification results.
        """
        print_section("⏸  HUMAN ACTION REQUIRED: Code Verification", style="yellow")

        console.print(f"[yellow bold]STEPS:[/yellow bold]\n")
        console.print(f"1. Open Gemini (https://gemini.google.com/ or use API)")
        console.print(f"2. Paste the contents of: [cyan]{prompt_file}[/cyan]")
        console.print(f"3. Copy Gemini's JSON response")
        console.print(f"4. Save it to: [cyan]{response_file}[/cyan]")
        console.print(f"5. Return here and confirm\n")

        console.print("[dim]Note: You can skip verification if you prefer (findings will be empty)[/dim]\n")

        # Ask if user wants to skip
        skip = confirm_action("Skip verification step?", default=False)

        if skip:
            console.print("[yellow]⚡ Skipping verification[/yellow]\n")
            return {
                "status": "skipped",
                "findings": [],
                "reason": "User chose to skip"
            }

        # Wait for response
        ready = confirm_action(
            f"Have you saved Gemini's response to {response_file.name}?",
            default=False
        )

        if not ready:
            return {
                "status": "cancelled",
                "findings": []
            }

        # Read and parse response
        if not response_file.exists():
            console.print(f"[red]Error: Response file not found: {response_file}[/red]")
            retry = confirm_action("Try again?", default=True)
            if retry:
                return self.wait_for_verification(prompt_file, response_file)
            return {"status": "no_file", "findings": []}

        try:
            response_text = response_file.read_text()
            findings = self._parse_findings(response_text)

            # Print findings
            self._print_verification_summary(findings)

            return {
                "status": "completed",
                "findings": findings,
                "findings_count": len(findings)
            }

        except Exception as e:
            console.print(f"[red]Error parsing verification response: {e}[/red]")
            return {"status": "parse_error", "findings": [], "error": str(e)}

    def _parse_findings(self, response_text: str) -> List[Dict[str, Any]]:
        """Parse Gemini's response into structured findings."""
        # Clean up response (remove markdown code blocks if present)
        text = response_text.strip()

        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        try:
            findings = json.loads(text)

            if not isinstance(findings, list):
                findings = [findings] if findings else []

            # Validate and normalize findings
            validated_findings = []
            for finding in findings:
                if isinstance(finding, dict):
                    validated_findings.append({
                        "severity": finding.get("severity", "MEDIUM"),
                        "category": finding.get("category", "General"),
                        "message": finding.get("message", "No message provided"),
                        "location": finding.get("location", "Unknown"),
                        "suggestion": finding.get("suggestion", "No suggestion provided")
                    })

            return validated_findings

        except json.JSONDecodeError:
            console.print("[yellow]⚠ Could not parse as JSON, assuming no issues[/yellow]")
            return []

    def _print_verification_summary(self, findings: List[Dict[str, Any]]) -> None:
        """Print a summary of verification findings."""
        console.print("\n[magenta bold]Verification Complete[/magenta bold]")

        if not findings:
            console.print("[green]✓ No issues found[/green]\n")
            return

        high = sum(1 for f in findings if f.get("severity") == "HIGH")
        medium = sum(1 for f in findings if f.get("severity") == "MEDIUM")
        low = sum(1 for f in findings if f.get("severity") == "LOW")

        console.print(f"\n[red]HIGH:[/red] {high}  [yellow]MEDIUM:[/yellow] {medium}  [blue]LOW:[/blue] {low}\n")

        print_findings(findings)