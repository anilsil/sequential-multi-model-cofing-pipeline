# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Agentic Code is a **prompt-based orchestrator** for governed multi-model coding workflows with separation of duties. Unlike traditional AI coding tools that make API calls, this tool generates prompts that users paste into accessible AI tools (Claude Code CLI, Cursor, Gemini) with full human-in-the-loop supervision.

**Core Philosophy**: Subscription-based tools (no pay-per-use), complete transparency, separation of duties, and human approval at every step.

**Architectural Note**: This is a **sequential multi-model pipeline** with governance, not a concurrent multi-agent system. While we use specialized "agents" (Claude, Codex, Gemini) in our code, they represent different **model roles** in a pipeline, not autonomous agents with emergent behavior. See the Architecture Overview section below for details.

## Development Commands

```bash
# Install in editable mode
pip install -e .

# Verify installation
agentic-code --version

# MANUAL MODE (prompt-based, requires copy-paste)
# Run example pipeline (skips verification for speed)
agentic-code run examples/simple-function.md --skip-verification

# Run with full verification
agentic-code run examples/simple-function.md

# Custom output directory
agentic-code run task.md --output /custom/path

# AUTOMATED MODE (uses Claude Code CLI - subscription-based!)
# Automates stages 1, 2, 5 using Claude CLI
python scripts/fully_automated.py examples/simple-function.md --skip-verification

# See AUTOMATION.md for full automation guide

# Development tools (if installed)
black agentic_code/        # Format code
ruff check agentic_code/   # Lint
mypy agentic_code/         # Type check
pytest                     # Run tests
```

## Architecture Overview

### Pipeline Flow (5-Stage Process)

The tool orchestrates a governed multi-model sequential workflow through **prompt generation**, not API calls. Each stage uses a different model for separation of duties:

1. **Stage 1: Repository Analysis** (Model: Claude - Analyst Role) → Generates analysis prompt → User pastes into Claude Code CLI → User saves response
2. **Stage 2: Task Planning** (Model: Claude - Planner Role) → Generates planning prompt → User pastes into Claude Code CLI → User saves YAML spec
3. **Stage 3: Code Implementation** (Model: Codex - Implementation Role) → Generates implementation prompt → User pastes into Cursor/IDE → User implements code
4. **Stage 4: Verification** [Optional] (Model: Gemini - Verification Role) → Generates verification prompt → User pastes into Gemini web → User saves JSON findings
5. **Stage 5: Integration Decision** (Model: Claude - Decision-Maker Role) → Generates decision prompt → User pastes into Claude Code CLI → User saves APPROVE/REJECT

**Key Principle**: Separation of duties - no model reviews its own work. Claude plans and decides, Codex implements, Gemini verifies. This is a **governance architecture**, not an emergent multi-agent system.

**Important Distinction**:
- ✅ This IS: A sequential multi-model pipeline with governance
- ✅ This IS: Separation of duties between different AI models
- ❌ This is NOT: A concurrent multi-agent system (e.g., Society of Mind)
- ❌ This is NOT: Emergent behavior from agent interactions
- ❌ This is NOT: Autonomous agents negotiating solutions

### Automation Mode (NEW!)

The tool now supports **fully automated execution** using Claude Code CLI programmatically:

**Manual Mode** (original):
- Generate prompt → User copies → Pastes into Claude CLI → Copies response → Pastes back

**Automated Mode** (new):
- Generate prompt → Automatically call `claude chat` → Capture response → Save automatically

**Subscription-based!** Uses Claude Code CLI (`claude chat --no-stream`) instead of pay-per-use Anthropic API. Requires Claude Pro subscription.

**How to use**:
```bash
python scripts/fully_automated.py examples/simple-function.md --skip-verification
```

Stages 1, 2, and 5 (Claude-based) are fully automated. Stage 3 (code implementation) remains manual for human oversight. See `AUTOMATION.md` for complete guide.

### Core Components

```
agentic_code/
├── cli.py                 # Typer CLI interface, main entry point
├── pipeline.py            # AgenticPipeline orchestrates 5-stage workflow
├── config.py              # Configuration (paths, settings) - NO API keys
├── utils.py               # File I/O, formatting, user confirmation helpers
└── agents/
    ├── claude.py          # Generates prompts for analysis, planning, decisions
    ├── codex.py           # Generates implementation prompts
    └── gemini.py          # Generates verification prompts
```

### Agent Responsibilities

**ClaudeAgent** (`agents/claude.py`):
- Generates repository analysis prompts (analyzes codebase structure)
- Generates task planning prompts (creates YAML implementation specs)
- Generates integration decision prompts (APPROVE/REJECT based on verification)
- Waits for user to paste responses from Claude Code CLI
- All prompts use templates: `REPO_ANALYSIS_PROMPT`, `TASK_PLANNING_PROMPT`, `INTEGRATION_DECISION_PROMPT`

**CodexAgent** (`agents/codex.py`):
- Generates implementation prompts (detailed code generation instructions)
- Waits for user to implement and save code to `generated_code/` directory
- Collects generated code files for verification step

**GeminiAgent** (`agents/gemini.py`):
- Generates verification prompts (security, logic errors, race conditions)
- Waits for user to paste JSON findings from Gemini web interface
- Parses and categorizes findings by severity (HIGH, MEDIUM, LOW)

### Configuration System

- **Config class** (`config.py`): Pydantic model with `output_dir`, `repo_root`, `skip_verification`, `require_human_approval`
- **No API keys**: This is a prompt orchestrator, not an API-based tool
- **Validation**: `validate_config()` ensures paths exist before pipeline runs
- **CLI overrides**: Command-line flags override default configuration

### Artifact Management

Every pipeline run creates a timestamped directory in `output/`:

```
output/YYYY-MM-DD_HHMMSS_task-name/
├── claude_analysis_prompt.md          # Prompt: What to paste
├── claude_analysis_response.txt       # Response: What you pasted back
├── claude_planning_prompt.md
├── claude_planning_response.yaml
├── task_spec.yaml                     # Extracted specification
├── codex_implementation_prompt.md
├── generated_code/                    # User-implemented code
│   ├── src/feature.py
│   └── tests/test_feature.py
├── gemini_verification_prompt.md      # Only if not --skip-verification
├── gemini_verification_response.json
├── verification_findings.json
├── claude_decision_prompt.md
├── claude_decision_response.yaml
└── integration_decision.yaml          # Final APPROVE/REJECT
```

**Critical**: All artifacts are plain text (Markdown, YAML, JSON) for version control and auditability.

## Key Design Patterns

### Human-in-the-Loop Pattern

- Every stage **requires user confirmation** before proceeding
- `wait_for_response()` blocks until user saves AI response to file
- `confirm_action()` utility prompts user with yes/no questions
- User can cancel pipeline at any stage (Ctrl+C)
- User can retry if response file is missing or empty

### Prompt Template Pattern

All agents use hardcoded prompt templates (e.g., `REPO_ANALYSIS_PROMPT`) with `.format()` placeholders:
- Templates are **visible in source code** (no hidden prompts)
- User can **edit generated prompts** before pasting them
- Templates enforce **consistent output formats** (YAML, JSON)

### Separation of Duties

| Agent | Plan | Implement | Verify | Decide |
|-------|------|-----------|--------|--------|
| Claude | ✓ | ✗ | ✗ | ✓ |
| Codex | ✗ | ✓ | ✗ | ✗ |
| Gemini | ✗ | ✗ | ✓ | ✗ |

**Never** let an agent review its own work. This prevents bias and creates audit trail.

### Task File Formats

Supports three formats (auto-detected by extension):

- **Markdown (.md)**: Freeform description with `# headers` and bullet points
- **YAML (.yaml)**: Structured with `name`, `objective`, `requirements`, `constraints`
- **JSON (.json)**: Same structure as YAML, but JSON format

`load_task_file()` in `utils.py` handles all three formats and extracts description.

## Development Guidelines

### Adding New Agents

1. Create agent class in `agentic_code/agents/new_agent.py`
2. Implement `generate_*_prompt()` methods that return prompt file paths
3. Implement `wait_for_*()` methods that block for user responses
4. Add agent to `pipeline.py` orchestration
5. Update `pyproject.toml` packages list if needed

### Modifying Prompts

**Never** modify prompts during runtime. All prompts are **hardcoded templates** in agent files:
- Edit `REPO_ANALYSIS_PROMPT`, `TASK_PLANNING_PROMPT`, etc. in `agents/claude.py`
- Edit `IMPLEMENTATION_PROMPT` in `agents/codex.py`
- Edit `VERIFICATION_PROMPT` in `agents/gemini.py`
- Prompts are formatted with `.format()` at generation time

### Error Handling

- **Missing response files**: Prompts user to retry
- **Empty response files**: Prompts user to retry
- **Invalid YAML/JSON**: Shows error, allows retry
- **Interrupted pipeline**: Graceful exit, preserves artifacts created so far
- **Invalid config**: Exits before pipeline starts with clear error messages

### CLI Design

- Uses **Typer** for CLI framework (type-safe, automatic help)
- Uses **Rich** for terminal formatting (colors, panels, tables)
- Main command: `run` (executes pipeline)
- Options: `--skip-verification`, `--output`
- Exit codes: 0 (approved), 1 (rejected/error), 130 (Ctrl+C)

## Important Constraints

### NO API CALLS

This tool **never** makes API calls to AI services. It only:
- Generates prompt files
- Waits for user to paste responses
- Reads response files from disk

If you add features, **never** introduce API dependencies (OpenAI, Anthropic SDKs, etc.).

### Human Approval Required

- `config.require_human_approval` is **always True** by design
- Never add "auto-execute" modes that bypass human review
- User must explicitly confirm each stage

### Artifact Preservation

- Never delete artifacts from previous runs
- Always create new timestamped directories
- All artifacts must be **plain text** (no binary formats)
- Preserve complete audit trail

### Python Version

- Requires **Python 3.11+** (uses modern type hints like `list[str]`)
- Uses `Path` objects (not strings) for file paths
- Uses Pydantic v2 models for configuration

## Common Development Tasks

### Testing the Pipeline

```bash
# Quick test (skip verification)
agentic-code run examples/simple-function.md --skip-verification

# Full test (includes Gemini verification)
agentic-code run examples/simple-function.md

# Test with custom output location
agentic-code run examples/simple-function.md --output /tmp/test-run
```

### Debugging Pipeline Issues

1. Check `output/YYYY-MM-DD_HHMMSS_task-name/` for generated artifacts
2. Review prompt files (`*_prompt.md`) to see what was generated
3. Review response files (`*_response.*`) to see what user provided
4. Check `task_spec.yaml` for parsed task specification
5. Look at `integration_decision.yaml` for final decision rationale

### Adding New Prompt Templates

1. Define template as module-level constant in agent file (e.g., `NEW_PROMPT = """..."""`)
2. Add `.format()` placeholders for dynamic content
3. Create `generate_*_prompt()` method that calls `save_artifact()`
4. Create `wait_for_*()` method that calls `wait_for_response()`
5. Add stage to `pipeline.py` orchestration

### Modifying Output Format

- **Prompts**: Edit Rich formatting in `utils.py` (`console.print()`)
- **Tables**: Use `rich.table.Table` (see artifact summary in `utils.py`)
- **Panels**: Use `rich.panel.Panel` (see CLI welcome message)
- **Progress**: Use `print_pipeline_status()` for stage updates

## Code Style

- **Line length**: 100 characters (configured in `pyproject.toml`)
- **Formatting**: Black (opinionated, no configuration needed)
- **Linting**: Ruff (fast Python linter)
- **Type checking**: mypy (lenient - `disallow_untyped_defs = false`)
- **String formatting**: f-strings or `.format()` (no `%` formatting)
- **Path handling**: Always use `pathlib.Path`, never string concatenation
- **Console output**: Use Rich (`console.print()` with color tags like `[cyan]text[/cyan]`)

## Dependencies

- **typer**: CLI framework (type-safe argument parsing)
- **rich**: Terminal formatting (colors, tables, progress)
- **pyyaml**: YAML parsing (for task specs and responses)
- **pydantic**: Data validation (for Config model)

**No AI SDKs** are included - this is intentional. The tool generates prompts, not API calls.
