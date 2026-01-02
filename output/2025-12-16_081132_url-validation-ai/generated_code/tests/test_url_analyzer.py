import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agentic_code.url_analyzer import URLAnalyzer, URLRateLimiter  # noqa: E402
from agentic_code.url_database import URLAnalysisDB  # noqa: E402


def test_spam_score_tracks_keywords_and_params():
    analyzer = URLAnalyzer()
    result = analyzer.analyze("https://example.com/path?utm_source=news&clickid=123")
    assert result.spam_score >= 0.3


def test_phishing_score_detects_brand_and_login():
    analyzer = URLAnalyzer()
    result = analyzer.analyze("https://secure-paypal.com/login")
    assert result.phishing_score >= 0.4


def test_malicious_score_for_executable_and_port():
    analyzer = URLAnalyzer()
    result = analyzer.analyze("http://192.168.0.1:445/evil.exe")
    assert result.malicious_score >= 0.7


def test_authenticity_boost_for_https_and_whitelist():
    analyzer = URLAnalyzer()
    result = analyzer.analyze("https://example.com")
    assert result.authenticity_score > 0.7
    assert result.is_whitelisted


def test_blacklist_flagging():
    analyzer = URLAnalyzer()
    result = analyzer.analyze("http://phish.example/login")
    assert result.is_blacklisted
    assert "blacklisted_domain" in result.issues


def test_rate_limiter_blocks_after_threshold():
    ticks = [0.0]

    def fake_time():
        return ticks[0]

    limiter = URLRateLimiter(max_per_minute=2, window_seconds=60, time_func=fake_time)
    analyzer = URLAnalyzer(rate_limiter=limiter)
    analyzer.check_rate_limit(2)
    with pytest.raises(RuntimeError):
        analyzer.check_rate_limit(1)


def test_database_persistence(tmp_path: Path):
    db_path = tmp_path / "output" / "analysis.db"
    db = URLAnalysisDB(db_path=db_path)
    analyzer = URLAnalyzer()
    results = analyzer.batch_analyze(["https://example.com"], save=True, db=db)
    assert results[0].is_valid
    stored = db.fetch_recent(limit=5)
    assert stored
    assert stored[0]["url"] == "https://example.com"


def test_integration_extract_to_analyze():
    analyzer = URLAnalyzer()
    text = "Check https://bit.ly/redirect?url=https%3A%2F%2Fsafe.example.com%2Flogin"
    results = analyzer.analyze_text(text)
    assert len(results) == 1
    assert "safe.example.com" in results[0].unwrapped_url
    assert results[0].spam_score > 0
