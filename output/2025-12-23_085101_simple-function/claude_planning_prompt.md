# Task Planning - Create Implementation Specification

You are a software architect creating a detailed implementation plan.

## Context
Based on my analysis of the repository, here's a comprehensive overview:

## Repository Analysis

**Primary Language**: Python 3.11+ (exclusively Python codebase)

**Project Type**: CLI tool - A prompt orchestration framework for governed multi-agent coding workflows

**Key Frameworks & Libraries**:
- **Typer**: CLI framework with type-safe argument parsing
- **Rich**: Terminal formatting (colors, panels, tables, progress indicators)
- **Pydantic**: Data validation and configuration management (v2)
- **PyYAML**: YAML parsing for task specifications and responses
- **Google Generative AI & Anthropic SDK**: Listed as dependencies but used for automated mode, not core functionality

**Code Organization**:
```
agentic_code/
├── cli.py                 # Typer CLI entry point
├── pipeline.py            # Manual AgenticPipeline orchestration
├── automated_pipeline.py  # AutomatedAgenticPipeline with API calls
├── config.py              # Pydantic configuration model
├── utils.py               # File I/O, formatting, user confirmation helpers
└── agents/
    ├── claude.py          # Prompt generation for analysis, planning, decisions
    ├── codex.py           # Implementation prompt generation
    └── gemini.py          # Verification prompt generation
```

**Testing Approach**: 
- Framework: pytest (>=7.0.0) in dev dependencies
- No tests currently in the main codebase (test files only found in `output/` generated code directories)
- Test mode available via `Config.test_mode` for automated confirmations

**Notable Patterns**:
- **Human-in-the-loop orchestration**: Every stage requires user confirmation and manual response pasting
- **Separation of duties**: Different agents for different roles (Claude plans/decides, Codex implements, Gemini verifies)
- **Artifact-based workflow**: All prompts and responses saved as plain text files (Markdown, YAML, JSON) for auditability
- **Prompt template pattern**: Hardcoded templates in agent files with `.format()` placeholders
- **Timestamped output directories**: Each run creates `YYYY-MM-DD_HHMMSS_task-name/` directory

**Key Dependencies**:
- Runtime: typer, rich, pyyaml, pydantic (>=2.0), google-generativeai, anthropic
- Development: pytest, black, ruff, mypy

**Code Style**:
- **Formatter**: Black with 100-character line length
- **Linter**: Ruff targeting Python 3.11
- **Type checking**: mypy (lenient - `disallow_untyped_defs = false`)
- **Naming**: Snake_case for functions/variables, PascalCase for classes
- **Paths**: Exclusively uses `pathlib.Path`, never string concatenation
- **Console output**: Rich library with color tags like `[cyan]text[/cyan]`
- **Docstrings**: Google-style docstrings for modules and public methods

**Architecture Philosophy**: This is a **prompt orchestrator**, not an API-based tool. The core workflow generates prompts for users to paste into free AI tools (Claude Code CLI, Cursor, Gemini web), with complete transparency and zero API costs in manual mode.

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
