# Task Planning - Create Implementation Specification

You are a software architect creating a detailed implementation plan.

## Context
**Repository Analysis: Agentic-Code**

**Primary Language(s)**: Python 3.11+ (exclusively)

**Project Type**: CLI tool - A command-line orchestrator for governed multi-agent coding workflows

**Key Frameworks**:
- Typer: CLI framework for command-line interface
- Rich: Terminal formatting and user interaction (panels, tables, prompts)
- Pydantic v2: Configuration validation and data models
- PyYAML: YAML parsing for task specifications and responses

**Code Organization**:
- `agentic_code/`: Main package directory
  - `cli.py`: Typer-based CLI entry point
  - `pipeline.py`: Core AgenticPipeline orchestration (5-stage workflow)
  - `config.py`: Pydantic configuration model
  - `utils.py`: File I/O, user confirmation, Rich formatting utilities
  - `agents/`: Agent modules (claude.py, codex.py, gemini.py)
- `examples/`: Task file examples (MD, YAML, JSON formats)
- `scripts/`: Automation scripts (fully_automated.py)
- `output/`: Generated artifacts from pipeline runs (timestamped directories)

**Testing Approach**: Pytest framework configured in optional dev dependencies. Tests would be located in a `tests/` directory (not yet present in the repository).

**Notable Patterns**:
- Prompt orchestration pattern (generates prompts, waits for human responses)
- Human-in-the-loop workflow with explicit confirmation at each stage
- Separation of duties (Claude plans/decides, Codex implements, Gemini verifies)
- Artifact preservation with timestamped output directories
- No API calls - 100% free prompt-based approach

**Dependencies**:
- Core: typer, rich, pyyaml, pydantic (minimal, no AI SDKs)
- Dev: pytest, black, ruff, mypy

**Code Style**:
- Line length: 100 characters (Black/Ruff enforced)
- Python 3.11+ features (modern type hints like `list[str]`)
- Pathlib.Path for file operations (never string paths)
- Rich console for all user output
- Snake_case naming convention
- Lenient mypy settings (disallow_untyped_defs = false)

## Task Description
# AI-Powered URL Validation System

Create a comprehensive URL validation system for detecting malicious, spam, and inauthentic URLs in user-generated content using AI agents.

## Objective

Implement an AI-powered URL validation and analysis system that integrates with the TrustLink AI Guardian platform to detect phishing attempts, spam URLs, malicious links, and assess URL authenticity in posts and messages.

## Requirements

### Core URL Validation
- Extract and validate URLs from post content and messages
- Validate URL format and structure (protocol, domain, path)
- Check for common URL obfuscation techniques (bit.ly redirects, URL shorteners)
- Detect suspicious TLDs and domains
- Handle edge cases (malformed URLs, international domains, encoded URLs)

### AI-Powered Analysis
- Integrate with existing `ai_post_analysis` table structure
- Add URL-specific analysis fields
- Generate AI analysis using pattern matching and heuristics
- Store URL analysis results with timestamps

### Security Features
- Blacklist checking against known malicious domains
- Whitelist support for verified safe domains
- Real-time URL reputation checking
- Detect homograph attacks (Unicode lookalike domains)
- Identify shortened URL chains and unwrap them safely
- Rate limiting for URL submissions

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
