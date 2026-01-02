import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agentic_code.url_validator import validate_url_format  # noqa: E402


def test_validate_accepts_https_domain():
    result = validate_url_format("https://example.com/path")
    assert result.is_valid
    assert result.domain == "example.com"
    assert result.reason is None


def test_rejects_invalid_scheme():
    result = validate_url_format("htp://bad")
    assert not result.is_valid
    assert result.reason == "invalid_scheme"


def test_rejects_javascript_scheme():
    result = validate_url_format("javascript:alert(1)")
    assert not result.is_valid
    assert result.reason == "disallowed_scheme"


def test_rejects_oversized_url():
    long_path = "a" * 2100
    result = validate_url_format(f"https://example.com/{long_path}")
    assert not result.is_valid
    assert result.reason == "empty_or_too_long"
