# URL Validation System Summary

## Files Created
- agentic_code/url_extractor.py
- agentic_code/url_validator.py
- agentic_code/url_analyzer.py
- agentic_code/url_database.py
- agentic_code/cli.py (extended with URL commands)
- agentic_code/__init__.py
- data/blacklist_domains.txt
- data/whitelist_domains.txt
- data/suspicious_keywords.txt
- tests/test_url_extractor.py
- tests/test_url_validator.py
- tests/test_url_analyzer.py

## Key Decisions
- Regex-based extraction supporting protocol-less domains; normalized to http for validation.
- Structured validation with scheme/domain checks, IDN tolerance, and guardrails against dangerous schemes.
- Heuristic scoring for spam/phishing/malicious/authenticity using keywords, tracking params, ports, executables, shortener detection, and homograph heuristics.
- Rate limiting via in-memory windowed counter; batch capped at 50 URLs.
- SQLite persistence with indexed domain/timestamp fields; JSON-encoded issues.
- Typer CLI commands: `analyze-url`, `batch-analyze`, `add-to-blacklist` with Rich table output.

## How to Run/ Test
- Install dev deps if needed, then run:
  - `python -m pytest agentic-code/output/2025-12-16_081132_url-validation-ai/generated_code/tests`
- CLI examples:
  - `python -m agentic_code.cli analyze-url "Check https://example.com"`
  - `python -m agentic_code.cli batch-analyze path/to/file.txt`
