"""
Agent implementations for the agentic coding pipeline.

Each agent has a strict, well-defined role:
- Claude: Architect, planner, integrator
- Codex: Implementation agent (human-in-the-loop)
- Gemini: Verification agent (no code generation)
"""

from .claude import ClaudeAgent
from .codex import CodexAgent
from .gemini import GeminiAgent

__all__ = ["ClaudeAgent", "CodexAgent", "GeminiAgent"]
