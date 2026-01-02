import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agentic_code.url_extractor import extract_urls, normalize_inputs  # noqa: E402


def test_extract_urls_from_mixed_text():
    text = (
        "Visit https://example.com/page?utm_source=test and "
        "check www.sample.net/docs. Markdown [link](https://foo.bar/login)."
    )
    urls = extract_urls(text)
    assert "https://example.com/page?utm_source=test" in urls
    assert "http://www.sample.net/docs" in urls
    assert "https://foo.bar/login" in urls


def test_extract_urls_handles_plain_domains():
    text = "Dangerous link: badsite.co/malware, safe: example.com/path."
    urls = extract_urls(text)
    assert "http://badsite.co/malware" in urls
    assert "http://example.com/path" in urls


def test_normalize_inputs_skips_empty_entries():
    values = ["https://one.com", None, "   ", "two.com"]
    normalized = normalize_inputs(values)
    assert normalized == ["https://one.com", "two.com"]
