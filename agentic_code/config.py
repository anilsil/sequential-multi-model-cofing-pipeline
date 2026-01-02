"""
Configuration management for agentic-code.

Handles paths and user settings. No API keys needed - this is a prompt orchestrator!
"""

import os
from pathlib import Path
from pydantic import BaseModel, Field


class Config(BaseModel):
    """Main configuration for agentic-code."""

    # Paths
    output_dir: Path = Field(default_factory=lambda: Path("output"))
    repo_root: Path = Field(default_factory=lambda: Path.cwd())

    # Pipeline settings
    require_human_approval: bool = True
    save_artifacts: bool = True

    # Execution mode
    skip_verification: bool = False  # Skip Gemini verification step
    test_mode: bool = False  # Enable test mode for automated confirmations and dummy responses
    implementation_cli_command: Optional[str] = None # Optional CLI command for implementation

    class Config:
        arbitrary_types_allowed = True


def load_config(output_dir: Path = None, repo_root: Path = None) -> Config:
    """
    Load configuration.

    Args:
        output_dir: Optional output directory override
        repo_root: Optional repo root override

    Returns:
        Config object with loaded settings
    """
    return Config(
        output_dir=output_dir or Path("output"),
        repo_root=repo_root or Path.cwd()
    )


def validate_config(config: Config) -> list[str]:
    """
    Validate configuration and return list of errors.

    Args:
        config: Configuration to validate

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    if not config.output_dir.parent.exists():
        errors.append(f"Output directory parent does not exist: {config.output_dir.parent}")

    if not config.repo_root.exists():
        errors.append(f"Repository root does not exist: {config.repo_root}")

    return errors
