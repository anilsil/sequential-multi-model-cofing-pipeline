"""
Agentic Code - Local-first, governed multi-model coding pipeline.

A CLI tool that orchestrates a sequential multi-model workflow with strict
separation of duties between planning (Claude), implementation (Codex), and
verification (Gemini).

Architecture: Sequential pipeline with governance, NOT concurrent multi-agent system.
"""

__version__ = "0.1.0"
