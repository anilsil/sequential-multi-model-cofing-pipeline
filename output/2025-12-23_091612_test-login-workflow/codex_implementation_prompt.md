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
task_name: test-login-workflow
objective: Create comprehensive automated test suite for user authentication login workflow covering happy paths, error handling, security scenarios, and edge cases
requirements:
  - Implement unit tests for login validation logic (email format, password requirements, input sanitization)
  - Implement integration tests for complete login flow (authentication, session creation, redirects)
  - Implement security tests for common vulnerabilities (XSS, SQL injection, rate limiting, password exposure)
  - Test error handling for invalid credentials, empty fields, non-existent users
  - Test edge cases including long inputs, special characters, simultaneous logins, expired sessions
  - Use existing pytest framework with fixtures and mocks
  - Mock external dependencies (database, Supabase Auth API calls)
  - Achieve >80% test coverage for login functionality
  - All tests must be isolated, repeatable, and fast (<5 seconds for unit tests)
  - Follow existing test patterns in codebase (pytest conventions, fixture usage)
files_to_modify:
  - None (only adding test files, no production code changes)
new_files:
  - tests/test_login_validation.py
  - tests/test_login_integration.py
  - tests/test_login_security.py
  - tests/fixtures/auth_fixtures.py
  - tests/conftest.py
  - tests/README.md
implementation_steps:
  - Step 1: Create pytest configuration in tests/conftest.py with shared fixtures (mock Supabase client, test users, auth responses)
  - Step 2: Create tests/fixtures/auth_fixtures.py with sample valid/invalid user data, authentication responses, and mock utilities
  - Step 3: Implement tests/test_login_validation.py for unit tests (email validation, password validation, input sanitization, empty field checks)
  - Step 4: Implement tests/test_login_integration.py for full login flow (successful login, session persistence, token storage, redirects, logout scenarios)
  - Step 5: Implement tests/test_login_security.py for security scenarios (XSS prevention, SQL injection blocking, rate limiting, password masking, secure error messages)
  - Step 6: Create tests/README.md documenting how to run tests, what each test file covers, and how to add new tests
  - Step 7: Run pytest with coverage report to verify >80% coverage target
  - Step 8: Ensure all tests pass and execute in <5 seconds for unit tests
testing_requirements:
  - All test files must use pytest framework with descriptive test names (test_valid_email_login_succeeds)
  - Use pytest fixtures for test data setup and teardown
  - Mock Supabase authentication API calls using pytest-mock or unittest.mock
  - Include pytest markers for test categories (@pytest.mark.unit, @pytest.mark.integration, @pytest.mark.security)
  - Test coverage report generated via pytest-cov plugin
  - Each test must have clear assertions with descriptive failure messages
  - Use parametrize decorator for testing multiple input variations efficiently
  - Include both positive and negative test cases for each requirement
  - Tests must clean up any test data/state after execution
constraints:
  - Do NOT modify any production code in src/ directory
  - Do NOT modify existing authentication logic or Supabase integration
  - Do NOT add new production dependencies (only dev/test dependencies like pytest-cov if missing)
  - Follow pytest naming conventions (test_*.py files, test_* functions)
  - Use existing mock patterns from codebase if any exist
  - Tests must be runnable via simple 'pytest' command
  - Do NOT commit sensitive credentials or API keys in test fixtures
  - Error messages in tests should not expose implementation details
  - Follow Python 3.11+ type hints in test code
  - Use pathlib.Path for file paths in tests if needed
  - Maintain test isolation (no test should depend on another test's execution)

## REPOSITORY CONTEXT:
Based on my analysis of the repository, here's a comprehensive overview:

## Repository Analysis

**1. Primary Language(s)**: Python 3.11+ exclusively

**2. Project Type**: CLI tool - a prompt orchestrator for governed multi-agent coding workflows

**3. Key Frameworks**:
- **Typer** (CLI framework with type-safe argument parsing)
- **Rich** (terminal formatting - colors, tables, panels, syntax highlighting)
- **Pydantic** (data validation and configuration management)
- **PyYAML** (YAML parsing for task specs and responses)
- **google-generativeai** & **anthropic** (for automated mode API calls)

**4. Code Organization**:
```
agentic_code/
├── cli.py                 # Typer CLI entry point
├── pipeline.py            # Manual pipeline orchestration (prompt-based)
├── automated_pipeline.py  # Automated pipeline (uses Claude CLI)
├── config.py              # Pydantic configuration model
├── utils.py               # Rich formatting, file I/O, user interactions
└── agents/
    ├── claude.py

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
