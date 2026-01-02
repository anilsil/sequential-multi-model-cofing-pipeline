#!/usr/bin/env python3
"""
Truly automated agentic-code pipeline using APIs.

This script automates the entire pipeline by:
1. Calling Claude and Gemini APIs directly.
2. No manual copy-paste needed.

Requirements:
- Claude and Gemini API keys set as environment variables.
- agentic-code package installed.

Usage:
    python scripts/truly_automated_pipeline.py examples/simple-function.md
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agentic_code.config import load_config
from agentic_code.automated_pipeline import AutomatedAgenticPipeline
from agentic_code.utils import console

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        console.print("[red]Usage: python scripts/truly_automated_pipeline.py <task-file>[/red]")
        console.print("\nExample:")
        console.print("  python scripts/truly_automated_pipeline.py examples/simple-function.md")
        sys.exit(1)

    task_path = Path(sys.argv[1])

    if not task_path.exists():
        console.print(f"[red]Task file not found: {task_path}[/red]")
        sys.exit(1)

    # Load config and run pipeline
    config = load_config()
    pipeline = AutomatedAgenticPipeline(config)
    results = pipeline.run(task_path)

    # Exit with appropriate code based on decision
    final_decision = results.get("final_decision", "UNKNOWN")
    if final_decision == "APPROVE":
        sys.exit(0)
    elif final_decision in ["REJECT", "ERROR", "PARSE_ERROR"]:
        sys.exit(1)
    else:
        sys.exit(0) # Approve with notes, etc.

if __name__ == "__main__":
    main()
