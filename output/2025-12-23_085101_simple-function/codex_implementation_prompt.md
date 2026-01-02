# Implementation Task

You are an implementation agent. Your ONLY job is to write clean, working code based on the specification.

## STRICT RULES:
1. Follow the task specification EXACTLY.
2. Follow existing repository patterns.
3. NO new dependencies unless specified.
4. Add tests for all new functionality.
5. Output code in the specified format ONLY.
6. DO NOT write any explanations or conversational text.

## TASK SPECIFICATION:
task_name: email-validation-utility
objective: Create a utility function to validate email addresses using regex with comprehensive test coverage
requirements:
  - Function named `validate_email` that accepts a string and returns boolean
  - Email validation using Python regex (re module from standard library)
  - Handle edge cases including empty strings, None values, and malformed formats
  - Function should validate standard RFC-compliant email formats
  - Include type hints for function signature
  - Add Google-style docstring with examples
  - Comprehensive pytest test suite with 100% coverage of edge cases
files_to_modify:
  - agentic_code/utils.py
new_files:
  - tests/test_email_validation.py
implementation_steps:
  - Step 1: Add `validate_email(email: str | None) -> bool` function to `agentic_code/utils.py` below existing utility functions
  - Step 2: Implement regex pattern for email validation (support standard formats like user@domain.com, name.last@domain.co.uk)
  - Step 3: Add None and empty string checks before regex validation
  - Step 4: Add comprehensive docstring with parameter description, return value, and usage examples
  - Step 5: Create `tests/test_email_validation.py` with pytest test class
  - Step 6: Add test cases for valid emails (simple, with dots, with hyphens, various TLDs)
  - Step 7: Add test cases for invalid emails (missing @, missing domain, missing local part, invalid characters)
  - Step 8: Add test cases for edge cases (None, empty string, whitespace-only, very long emails >254 chars)
  - Step 9: Run pytest to verify all tests pass
testing_requirements:
  - Test valid formats: user@example.com, name.last@domain.co.uk, user+tag@example.com, user123@sub.domain.com
  - Test invalid formats: @example.com, user@, no-at-sign.com, user@domain, user@@domain.com
  - Test edge cases: None, empty string "", whitespace "  ", extremely long email (>254 chars)
  - Verify function returns True for all valid cases
  - Verify function returns False for all invalid and edge cases
  - Achieve 100% code coverage for the validate_email function
constraints:
  - Do NOT add external dependencies (use only Python standard library `re` module)
  - Follow existing code style in utils.py (Black formatting, 100 char line length)
  - Use pathlib.Path pattern if file path handling is needed (not applicable here)
  - Add type hints matching existing utils.py patterns (use `str | None` for optional strings)
  - Place function logically in utils.py near other validation/helper functions
  - Do NOT modify existing functions in utils.py
  - Follow pytest naming conventions (test_*.py file, test_* functions)
  - Use descriptive test function names (test_validate_email_valid_simple_format, test_validate_email_none_input, etc)

## REPOSITORY CONTEXT:
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
├── utils.py              

## OUTPUT REQUIREMENTS:
You MUST output the code for each file using the following format. Do not add any other text or explanations.

-- FILE: path/to/your/file.py --
```python
# Your code here
```
-- ENDFILE --

-- FILE: path/to/your/test_file.py --
```python
# Your test code here
```
-- ENDFILE --

-- FILE: summary.md --
```markdown
### Implementation Summary
- **Files Created**: `path/to/your/file.py`, `path/to/your/test_file.py`
- **Key Decisions**: Brief explanation of any choices made.
- **How to Run**: Instructions on how to run or test the new code.
```
-- ENDFILE --

BEGIN IMPLEMENTATION NOW.
