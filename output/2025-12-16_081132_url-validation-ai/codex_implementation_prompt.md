# Implementation Task for Codex

You are an implementation agent. Your ONLY job is to write clean, working code.

## STRICT RULES:
1. Follow the task specification EXACTLY
2. Follow existing repository patterns
3. NO new dependencies unless specified in task spec
4. Add tests for all new functionality
5. Output CODE ONLY - no explanations, no reviews, no verification
6. DO NOT modify files outside the scope
7. DO NOT auto-commit or auto-merge

## TASK SPECIFICATION:
```yaml
task_name: url-validation-system
objective: Implement AI-powered URL validation system for detecting malicious, spam, and phishing URLs in user content
requirements:
  - Extract URLs from text content using regex patterns
  - Validate URL format (protocol, domain, path, query parameters)
  - Detect URL obfuscation techniques (shorteners, redirects, homographs)
  - Calculate spam, phishing, malicious, and authenticity scores (0-1 scale)
  - Support blacklist/whitelist domain checking
  - Handle edge cases (international domains, encoded URLs, IP addresses)
  - Rate limiting for URL analysis requests
  - Store URL analysis results with metadata
  - Provide CLI commands for URL analysis
files_to_modify:
  - agentic_code/cli.py
new_files:
  - agentic_code/url_validator.py
  - agentic_code/url_analyzer.py
  - agentic_code/url_extractor.py
  - agentic_code/url_database.py
  - tests/test_url_validator.py
  - tests/test_url_analyzer.py
  - tests/test_url_extractor.py
  - data/blacklist_domains.txt
  - data/whitelist_domains.txt
  - data/suspicious_keywords.txt
implementation_steps:
  - "Step 1: Create url_extractor.py with extract_urls() function using regex to find URLs in text"
  - "Step 2: Create url_validator.py with validate_url_format() for structural validation"
  - "Step 3: Create url_analyzer.py with AI scoring functions (calculate_spam_score, calculate_phishing_score, calculate_malicious_score, calculate_authenticity_score)"
  - "Step 4: Implement detect_homograph_attack() for Unicode lookalike domain detection"
  - "Step 5: Implement detect_url_shorteners() to identify and unwrap shortened URLs"
  - "Step 6: Create url_database.py with URLAnalysisDB class for storing analysis results using SQLite"
  - "Step 7: Add domain blacklist/whitelist checking in url_analyzer.py"
  - "Step 8: Create data files (blacklist_domains.txt, whitelist_domains.txt, suspicious_keywords.txt)"
  - "Step 9: Add CLI commands to cli.py using Typer (analyze-url, batch-analyze, add-to-blacklist)"
  - "Step 10: Implement rate limiting using simple time-based counter"
  - "Step 11: Add Rich formatting for URL analysis output (colored scores, warning badges)"
  - "Step 12: Create comprehensive unit tests for all modules"
testing_requirements:
  - Test URL extraction from various text formats (plain text, markdown, HTML-like)
  - Test URL format validation (valid: https://example.com, invalid: htp://bad, javascript:alert)
  - Test spam detection heuristics (tracking parameters, suspicious keywords, redirects)
  - Test phishing detection (homograph attacks, brand impersonation patterns)
  - Test malicious URL detection (executable extensions, suspicious ports, IP addresses)
  - Test authenticity scoring (HTTPS presence, domain age indicators, TLD reputation)
  - Test blacklist/whitelist matching (exact domain, subdomain wildcards)
  - Test edge cases (very long URLs >2000 chars, international domains, URL-encoded content)
  - Test rate limiting (exceed limit should return error)
  - Test database storage and retrieval of analysis results
  - Integration test: full pipeline from text input to scored output
constraints:
  - Do NOT add external API dependencies (no requests, httpx, etc.)
  - Do NOT make network calls for real-time URL checking (offline analysis only)
  - Follow existing Typer CLI pattern from cli.py
  - Use Pathlib.Path for file operations (never string paths)
  - Use Rich console for output formatting (match existing style)
  - Line length max 100 characters (Black/Ruff compliance)
  - Use Python 3.11+ type hints (list[str] not List[str])
  - Store data files in data/ directory at repository root
  - Use SQLite for URL analysis database (store in output/ directory)
  - Follow snake_case naming convention throughout
  - No modification to existing agents/ directory
  - Maintain backward compatibility with existing CLI commands
security_considerations:
  - Sanitize all URL inputs to prevent code injection
  - Never execute or follow URLs automatically
  - Validate file paths for blacklist/whitelist to prevent directory traversal
  - Use parameterized queries for SQLite to prevent SQL injection
  - Rate limit: max 100 URLs per minute per session
  - Log suspicious patterns but don't expose detection logic details
performance_requirements:
  - Single URL analysis must complete within 100ms
  - Batch analysis: support up to 50 URLs per request
  - Domain blacklist lookup using set() for O(1) performance
  - Cache compiled regex patterns for URL extraction
  - Database queries should use indexes on timestamp and domain fields
```

## REPOSITORY CONTEXT:
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

## OUTPUT REQUIREMENTS:
- Write all code to: /Users/anilsharma/webkins/trustlink-aigardian-main/agentic-code/output/2025-12-16_081132_url-validation-ai/generated_code/
- Create directory structure as needed
- Include tests in appropriate test directory
- Use existing code style and patterns

## WHAT TO GENERATE:
1. Implementation files (as specified in task_spec)
2. Test files
3. A summary.md file listing:
   - Files created
   - Files modified
   - Key implementation decisions
   - How to run/test the code

BEGIN IMPLEMENTATION NOW.
