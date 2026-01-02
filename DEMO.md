# Step-by-Step Demo: Automated Agentic Code

This guide shows **exactly** what happens when you run the automated pipeline on a real example.

## 📝 Example Task

We'll implement an email validation function using:
```bash
python scripts/fully_automated.py examples/simple-function.md --skip-verification
```

**Task File**: `examples/simple-function.md`
```markdown
# Add Email Validation Function

Create a utility function to validate email addresses.

## Requirements
- Function should accept a string and return boolean
- Validate email format using regex
- Handle edge cases (empty string, null, invalid formats)
- Add comprehensive unit tests
```

---

## 🚀 What Happens: The Complete Flow

### Initial Command

```bash
$ python scripts/fully_automated.py examples/simple-function.md --skip-verification
```

### Console Output

```
🚀 FULLY AUTOMATED AGENTIC CODE (FREE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Task: examples/simple-function.md
Mode: Claude Code CLI (100% Free)
Automation: Fully automated (no manual steps)

Run directory: output/2025-12-15_231245_simple-function
```

---

## 📊 STAGE 1: Repository Analysis

### What the Script Does

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏳ Stage 1: Repository Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Behind the scenes:**

1. **Generates analysis prompt** and saves to:
   - `output/.../claude_analysis_prompt.md`

2. **Prompt content** (what gets sent to Claude):
```markdown
# Repository Analysis Task

You are analyzing a codebase to understand its structure and patterns.

## Repository Information
- Location: /Users/anilsharma/webkins/trustlink-aigardian-main/agentic-code
- Purpose: Understand existing patterns before implementing new features

## Your Task
Analyze this repository and provide:

1. **Primary Language(s)**: What languages are primarily used?
2. **Project Type**: Web app, CLI tool, library, etc.
3. **Key Frameworks**: What major frameworks/libraries are in use?
4. **Code Organization**: How is the code structured?
5. **Testing Approach**: What testing framework is used?
6. **Notable Patterns**: Any architectural patterns?
7. **Dependencies**: Key dependencies from package files
8. **Code Style**: Naming conventions, formatting preferences

## Output Format
Provide a concise analysis (200-300 words) focusing on facts that
would help implement new features consistently with existing patterns.

**Begin your analysis:**
```

3. **Calls Claude CLI automatically**:
```python
subprocess.run(
    ["claude", "chat", "--no-stream"],
    input=prompt,
    capture_output=True
)
```

4. **Claude CLI responds** (this is FREE - no API key!):
```
🤖 Calling Claude Code CLI...
✓ Received response (1,234 characters)
```

5. **Response saved automatically** to:
   - `output/.../claude_analysis_response.txt`

**Example Response from Claude**:
```
This is a Python-based CLI tool built with the following characteristics:

**Primary Language**: Python 3.11+

**Project Type**: Command-line tool (CLI) for orchestrating multi-agent
coding workflows

**Key Frameworks**:
- Typer (CLI framework)
- Rich (terminal formatting)
- Pydantic (data validation)
- PyYAML (configuration)

**Code Organization**:
- `agentic_code/` - Main package
  - `cli.py` - CLI entry point
  - `pipeline.py` - Orchestration logic
  - `agents/` - Agent implementations (claude, codex, gemini)
  - `utils.py` - Helper functions

**Testing Approach**: No tests found yet (opportunity to add pytest)

**Notable Patterns**:
- Agent-based architecture with separation of duties
- Prompt-based orchestration (no API calls)
- Human-in-the-loop validation
- Artifact preservation for audit trails

**Dependencies**:
- typer>=0.9.0, rich>=13.0.0, pyyaml>=6.0, pydantic>=2.0.0

**Code Style**:
- Black formatting (line length: 100)
- Type hints (Python 3.11+ style)
- Path objects over strings
- Rich console for output
```

**Result**: ✅ Stage 1 completed automatically in ~5 seconds

---

## 📝 STAGE 2: Task Planning

### What the Script Does

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏳ Stage 2: Task Planning
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

1. **Generates planning prompt** combining:
   - Repository analysis from Stage 1
   - Original task description

2. **Prompt content**:
```markdown
# Task Planning - Create Implementation Specification

## Context
[Full repository analysis from Stage 1]

## Task Description
# Add Email Validation Function

Create a utility function to validate email addresses.

Requirements:
- Function should accept a string and return boolean
- Validate email format using regex
- Handle edge cases (empty string, null, invalid formats)
- Add comprehensive unit tests

## Your Job
Create a YAML specification that a developer can follow to implement this task.

## Required YAML Structure
```yaml
task_name: brief-descriptive-name
objective: One sentence describing the goal
requirements:
  - Specific requirement 1
  - Specific requirement 2
files_to_modify:
  - path/to/file1.ext
new_files:
  - path/to/new_file1.ext
implementation_steps:
  - Step 1: Description
  - Step 2: Description
testing_requirements:
  - Test requirement 1
constraints:
  - Do NOT modify X
  - Follow pattern Y
```

## Critical Guidelines
- Be SPECIFIC about file paths and locations
- Follow existing repository patterns (from analysis above)
- Minimize scope - only what's truly necessary
- No new dependencies unless absolutely critical

**Output ONLY the YAML specification (no markdown code blocks):**
```

3. **Calls Claude CLI**:
```
🤖 Calling Claude Code CLI...
✓ Received response (892 characters)
```

4. **Response saved** to:
   - `output/.../claude_planning_response.yaml`
   - `output/.../task_spec.yaml`

**Example Response (YAML)**:
```yaml
task_name: add-email-validation
objective: Create a utility function to validate email addresses with comprehensive tests

requirements:
  - Accept string input and return boolean
  - Use regex pattern for RFC-compliant email validation
  - Handle edge cases: empty strings, null values, malformed addresses
  - Provide clear validation error messages
  - Include comprehensive unit tests

files_to_modify: []

new_files:
  - agentic_code/validators.py
  - tests/test_validators.py

implementation_steps:
  - Step 1: Create validators.py module in agentic_code/
  - Step 2: Implement validate_email() function with regex pattern
  - Step 3: Add edge case handling (None, empty, whitespace)
  - Step 4: Create test_validators.py with pytest
  - Step 5: Add tests for valid emails (user@domain.com, name+tag@example.co.uk)
  - Step 6: Add tests for invalid emails (@domain, user@, no-at-sign, multiple@at@signs)
  - Step 7: Add edge case tests (None, empty string, very long strings)

testing_requirements:
  - Use pytest framework (already in dev dependencies)
  - Minimum 90% code coverage for validators.py
  - Test all edge cases explicitly
  - Include docstring examples for doctest

constraints:
  - Do NOT add external dependencies (use stdlib re module)
  - Follow existing code style (Black, 100 char lines)
  - Use type hints (Python 3.11+ style)
  - Match existing utils.py patterns for function structure
```

**Result**: ✅ Stage 2 completed automatically in ~8 seconds

---

## 💻 STAGE 3: Code Implementation (MANUAL)

### What the Script Does

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏸  Stage 3: Code Generation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

1. **Generates implementation prompt**:
```markdown
# Implementation Task for Codex

Follow this specification exactly:

```yaml
[Full task spec from Stage 2]
```

## Instructions
1. Implement ALL files listed in the specification
2. Follow the implementation steps in order
3. Save all code to: output/.../generated_code/
4. Create a summary.md with what you implemented

## Code Requirements
- Match the existing code style from repository analysis
- Use type hints (Python 3.11+)
- Add docstrings
- Follow all constraints

**Output CODE ONLY. Start implementing now.**
```

2. **Pauses for human**:
```
⏸  MANUAL STEP REQUIRED

Please implement the code as specified in:
  output/2025-12-15_231245_simple-function/codex_implementation_prompt.md

Save generated code to:
  output/2025-12-15_231245_simple-function/generated_code/

Press Enter when code is ready...
```

### What YOU Do

**Option A: Use Cursor/Copilot**
1. Open the prompt file in your IDE
2. Paste into Cursor/Copilot
3. Let it generate the code
4. Save to `generated_code/` directory

**Option B: Write Manually**
1. Read the spec in `task_spec.yaml`
2. Implement yourself
3. Save to `generated_code/` directory

**Example Implementation**:

File: `generated_code/agentic_code/validators.py`
```python
"""Email validation utilities."""

import re
from typing import Optional


def validate_email(email: Optional[str]) -> bool:
    """
    Validate email address format.

    Args:
        email: Email address to validate

    Returns:
        True if valid email format, False otherwise

    Examples:
        >>> validate_email("user@example.com")
        True
        >>> validate_email("invalid@")
        False
        >>> validate_email(None)
        False
    """
    if not email or not isinstance(email, str):
        return False

    email = email.strip()

    if not email:
        return False

    # RFC 5322 simplified pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    return bool(re.match(pattern, email))
```

File: `generated_code/tests/test_validators.py`
```python
"""Tests for email validation."""

import pytest
from agentic_code.validators import validate_email


def test_valid_emails():
    """Test valid email formats."""
    assert validate_email("user@example.com") is True
    assert validate_email("name.last@domain.co.uk") is True
    assert validate_email("user+tag@example.com") is True


def test_invalid_emails():
    """Test invalid email formats."""
    assert validate_email("@example.com") is False
    assert validate_email("user@") is False
    assert validate_email("no-at-sign.com") is False
    assert validate_email("multiple@@domain.com") is False


def test_edge_cases():
    """Test edge cases."""
    assert validate_email(None) is False
    assert validate_email("") is False
    assert validate_email("   ") is False
    assert validate_email("a" * 1000 + "@example.com") is True
```

3. **Press Enter** to continue the pipeline

**Result**: ✅ Stage 3 completed (manual implementation)

---

## ✅ STAGE 4: Verification (SKIPPED)

```
⚡ Skipping verification (as requested)
```

**Why skipped?**: We used `--skip-verification` flag for faster execution.

**If not skipped**: Would generate verification prompt for Gemini to check:
- Security issues
- Logic errors
- Race conditions
- Best practices
- Performance concerns

---

## ⚖️ STAGE 5: Integration Decision

### What the Script Does

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏳ Stage 5: Integration Decision
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

1. **Generates decision prompt**:
```markdown
# Integration Decision - Review and Approve/Reject

## Original Task Specification
```yaml
[Full task spec]
```

## Verification Findings
No issues found - code passed all checks.

## Your Decision
Review the verification findings and decide:

1. **APPROVE** - Code meets quality standards, safe to integrate
2. **REJECT** - Critical issues found, must fix before integration
3. **APPROVE_WITH_NOTES** - Minor issues, can integrate with caveats

## Required Output Format (YAML)
```yaml
decision: APPROVE | REJECT | APPROVE_WITH_NOTES
rationale: |
  Clear explanation of why you made this decision.

required_fixes:  # Only if REJECT
  - Fix 1

recommended_improvements:  # Optional
  - Improvement 1

integration_notes:  # Important caveats
  - Note 1
```

**Output ONLY the YAML decision (no markdown code blocks):**
```

2. **Calls Claude CLI**:
```
🤖 Calling Claude Code CLI...
✓ Received response (456 characters)
```

3. **Response saved** to:
   - `output/.../claude_decision_response.yaml`
   - `output/.../integration_decision.yaml`

**Example Response**:
```yaml
decision: APPROVE

rationale: |
  The email validation implementation meets all specified requirements:

  1. Uses stdlib regex (no external dependencies) ✓
  2. Handles edge cases (None, empty, whitespace) ✓
  3. Follows existing code style (type hints, docstrings) ✓
  4. Comprehensive tests with good coverage ✓
  5. RFC 5322 compliant pattern ✓

  No security issues or logic errors found. Code is production-ready.

required_fixes: []

recommended_improvements:
  - Consider adding email domain validation (MX record check) as optional feature
  - Could add more sophisticated pattern for international domains

integration_notes:
  - Remember to run pytest after integration
  - Add validators.py to __init__.py exports if needed
```

**Result**: ✅ Stage 5 completed automatically in ~6 seconds

---

## 📊 Final Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚖️  INTEGRATION DECISION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Decision: APPROVE

rationale: |
  The email validation implementation meets all specified requirements...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 PIPELINE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Status: Completed
Task: simple-function
Duration: 32.7s
Decision: APPROVE

Run directory: output/2025-12-15_231245_simple-function
```

---

## 📦 Files Created (Audit Trail)

```
output/2025-12-15_231245_simple-function/
├── claude_analysis_prompt.md          # What we asked (Stage 1)
├── claude_analysis_response.txt       # What Claude said (Stage 1)
├── claude_planning_prompt.md          # What we asked (Stage 2)
├── claude_planning_response.yaml      # What Claude said (Stage 2)
├── task_spec.yaml                     # Parsed specification
├── codex_implementation_prompt.md     # What we asked (Stage 3)
├── generated_code/                    # What YOU implemented
│   ├── agentic_code/
│   │   └── validators.py
│   └── tests/
│       └── test_validators.py
├── claude_decision_prompt.md          # What we asked (Stage 5)
├── claude_decision_response.yaml      # What Claude said (Stage 5)
└── integration_decision.yaml          # Final decision
```

**All artifacts preserved for audit trail!**

---

## ⏱️ Time Breakdown

| Stage | Mode | Time |
|-------|------|------|
| 1. Repository Analysis | 🤖 Automated | ~5s |
| 2. Task Planning | 🤖 Automated | ~8s |
| 3. Code Implementation | 👤 Manual | ~15s |
| 4. Verification | ⚡ Skipped | 0s |
| 5. Integration Decision | 🤖 Automated | ~6s |
| **Total** | | **~34s** |

**Manual time**: ~15s (just implementing code)
**Automated time**: ~19s (Claude CLI calls - FREE!)

---

## 💰 Cost Breakdown

| Stage | Tool Used | Cost |
|-------|-----------|------|
| 1. Analysis | Claude Code CLI | **$0.00** |
| 2. Planning | Claude Code CLI | **$0.00** |
| 3. Implementation | Your IDE | **$0.00** |
| 4. Verification | Skipped | **$0.00** |
| 5. Decision | Claude Code CLI | **$0.00** |
| **TOTAL** | | **$0.00** |

**Compare to API mode**: ~$0.15 per task = **You just saved $0.15!**
**Run 100 tasks**: You save **$15**
**Run 1000 tasks**: You save **$150**

---

## 🎯 Key Takeaways

### ✅ What Got Automated
- Repository analysis (Claude CLI)
- Task planning (Claude CLI)
- Integration decision (Claude CLI)
- File management (automatic)
- Artifact preservation (automatic)

### 👤 What Stayed Manual
- Code implementation (YOU in your IDE)
- Verification (optional Gemini web)

### 🎉 Benefits
1. **No window switching** - Script handles everything
2. **No copy-paste** - Automated CLI calls
3. **Complete audit trail** - Every prompt and response saved
4. **100% FREE** - Uses Claude Code CLI, not APIs
5. **Fast execution** - ~34s total, ~19s automated

### 🚀 Next Steps

1. **Review the decision**: Check `integration_decision.yaml`
2. **Run the tests**: `pytest generated_code/tests/`
3. **Integrate the code**: Copy from `generated_code/` to your repo
4. **Commit with confidence**: Complete audit trail proves compliance

---

## 🔄 Run It Yourself

```bash
# Try the same example
python scripts/fully_automated.py examples/simple-function.md --skip-verification

# Or create your own task
cat > my-task.md << 'EOF'
# Add Logging Utility

Create a logging utility with colored output.

## Requirements
- Support INFO, WARNING, ERROR levels
- Add timestamps
- Use Rich for colors
EOF

python scripts/fully_automated.py my-task.md --skip-verification
```

**That's it!** Fully automated, governed, auditable coding - **100% FREE**! 🎉
