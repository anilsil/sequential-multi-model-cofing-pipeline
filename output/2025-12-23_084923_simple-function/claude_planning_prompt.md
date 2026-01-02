# Task Planning - Create Implementation Specification

You are a software architect creating a detailed implementation plan.

## Context
Based on my comprehensive analysis of the agentic-code repository, here's my assessment:

---

## Repository Analysis

### 1. **Primary Language(s)**
Python 3.11+ (exclusive)

### 2. **Project Type**
CLI tool - A prompt orchestrator for governed multi-agent coding workflows. It's a meta-tool that generates prompts for AI assistants rather than making direct API calls.

### 3. **Key Frameworks**
- **Typer** (CLI framework)
- **Rich** (terminal formatting/UI)
- **Pydantic v2** (configuration validation)
- **PyYAML** (YAML parsing)
- Optional: `google-generativeai`, `anthropic` (for automated mode)

### 4. **Code Organization**
```
agentic_code/           # Main package
├── cli.py             # Typer CLI entry point
├── pipeline.py        # Manual orchestration (prompt-based)
├── automated_pipeline.py  # Automated orchestration (API-based)
├── config.py          # Pydantic configuration models
├── utils.py           # File I/O, Rich formatting, confirmations
└── agents/            # Agent modules
    ├── claude.py      # Analysis, planning, decisions
    ├── codex.py       # Implementation prompts
    └── gemini.py      # Verification prompts
```

### 5. **Testing Approach**
- **Framework**: pytest (in dev dependencies)
- **Location**: No tests directory exists yet (tests expected in `tests/`)
- **Current state**: Test infrastructure configured but not implemented

### 6. **Notable Patterns**
- **Orchestration Pattern**: 5-stage pipeline (analyze → plan → implement → verify → decide)
- **Human-in-the-Loop**: Every stage requires explicit human approval via file-based communication
- **Separation of Duties**: Different AI agents handle different stages (no self-review)
- **Artifact-First Design**: All prompts/responses saved as timestamped plain text files
- **Dual-Mode Architecture**: Manual (prompt-based, free) vs. Automated (API-based, programmatic)

### 7. **Dependencies**
**Core**: typer, rich, pyyaml, pydantic
**Optional AI SDKs**: google-generativeai, anthropic (only for automated mode)
**Dev Tools**: pytest, black, ruff, mypy

### 8. **Code Style**
- **Line length**: 100 chars (Black/Ruff configured)
- **Naming**: `snake_case` for functions/variables, `PascalCase` for classes
- **Type hints**: Modern Python 3.11+ syntax (`list[str]`, not `List[str]`)
- **Paths**: Exclusively `pathlib.Path` objects, never string concatenation
- **Output**: Rich console with color tags (`[cyan]text[/cyan]`)
- **Docstrings**: Module-level and class-level descriptions present

### Key Implementation Notes
When adding features: (1) Use Pydantic models for configuration, (2) Save all artifacts via `utils.save_artifact()`, (3) Use Rich console for user feedback, (4) Follow the template pattern for prompts (hardcoded with `.format()`), (5) Maintain timestamped output directories for auditability.

## Task Description
# Add Email Validation Function

Create a utility function to validate email addresses.

## Requirements

- Function should accept a string and return boolean
- Validate email format using regex
- Handle edge cases (empty string, null, invalid formats)
- Add comprehensive unit tests

## Constraints

- Use existing utility file pattern (if exists)
- No external dependencies for validation
- Follow existing code style

## Testing

- Test valid emails: user@example.com, name.last@domain.co.uk
- Test invalid emails: @example.com, user@, no-at-sign.com
- Test edge cases: empty, null, very long emails


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
