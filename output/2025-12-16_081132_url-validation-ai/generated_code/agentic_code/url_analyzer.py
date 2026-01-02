from __future__ import annotations

import json
import time
import unicodedata
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable
from urllib.parse import parse_qs, unquote, urlparse

from rich.console import Console
from rich.table import Table

from .url_extractor import extract_urls, normalize_inputs
from .url_validator import URLValidationResult, validate_url_format

console = Console()

DEFAULT_DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DEFAULT_DB_PATH = Path(__file__).resolve().parents[3] / "url_analysis.db"

SHORTENER_DOMAINS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "ow.ly",
    "buff.ly",
    "cutt.ly",
    "is.gd",
    "rebrand.ly",
    "lnkd.in",
}

SUSPICIOUS_TLDS = {
    "zip",
    "xyz",
    "top",
    "gq",
    "work",
    "country",
    "stream",
    "click",
}

SUSPICIOUS_PORTS = {21, 23, 445, 3389, 1337}
EXECUTABLE_EXTENSIONS = {".exe", ".scr", ".bat", ".cmd", ".ps1", ".apk", ".msi", ".bin"}
PHISHING_KEYWORDS = {"login", "verify", "secure", "account", "update", "password", "bank"}


@dataclass
class URLAnalysisResult:
    url: str
    normalized_url: str
    unwrapped_url: str
    domain: str | None
    is_valid: bool
    reason: str | None
    spam_score: float
    phishing_score: float
    malicious_score: float
    authenticity_score: float
    is_blacklisted: bool
    is_whitelisted: bool
    issues: list[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "normalized_url": self.normalized_url,
            "unwrapped_url": self.unwrapped_url,
            "domain": self.domain,
            "is_valid": self.is_valid,
            "reason": self.reason,
            "spam_score": self.spam_score,
            "phishing_score": self.phishing_score,
            "malicious_score": self.malicious_score,
            "authenticity_score": self.authenticity_score,
            "is_blacklisted": self.is_blacklisted,
            "is_whitelisted": self.is_whitelisted,
            "issues": self.issues,
            "timestamp": self.timestamp,
        }


class URLRateLimiter:
    def __init__(
        self,
        max_per_minute: int = 100,
        window_seconds: int = 60,
        time_func: callable = time.monotonic,
    ):
        self.max_per_minute = max_per_minute
        self.window_seconds = window_seconds
        self.time_func = time_func
        self._timestamps: deque[float] = deque()

    def _evict(self, now: float) -> None:
        cutoff = now - self.window_seconds
        while self._timestamps and self._timestamps[0] < cutoff:
            self._timestamps.popleft()

    def allow(self, count: int = 1) -> bool:
        now = self.time_func()
        self._evict(now)
        if len(self._timestamps) + count > self.max_per_minute:
            return False
        for _ in range(count):
            self._timestamps.append(now)
        return True


class URLAnalyzer:
    def __init__(
        self,
        data_dir: Path | None = None,
        blacklist_path: Path | None = None,
        whitelist_path: Path | None = None,
        suspicious_keywords_path: Path | None = None,
        rate_limiter: URLRateLimiter | None = None,
    ):
        self.data_dir = data_dir or DEFAULT_DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.blacklist = self._load_domain_set(
            blacklist_path or self.data_dir / "blacklist_domains.txt"
        )
        self.whitelist = self._load_domain_set(
            whitelist_path or self.data_dir / "whitelist_domains.txt"
        )
        self.suspicious_keywords = self._load_keyword_set(
            suspicious_keywords_path or self.data_dir / "suspicious_keywords.txt"
        )
        self.rate_limiter = rate_limiter or URLRateLimiter()

    def _safe_resolve(self, file_path: Path) -> Path:
        resolved = file_path.resolve()
        if self.data_dir not in resolved.parents and resolved != self.data_dir:
            raise ValueError("Unsafe data path")
        return resolved

    def _load_domain_set(self, file_path: Path) -> set[str]:
        resolved = self._safe_resolve(file_path)
        if not resolved.exists():
            return set()
        return {
            line.strip().lower()
            for line in resolved.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }

    def _load_keyword_set(self, file_path: Path) -> set[str]:
        resolved = self._safe_resolve(file_path)
        if not resolved.exists():
            return set()
        return {
            line.strip().lower()
            for line in resolved.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }

    def check_rate_limit(self, count: int) -> None:
        if not self.rate_limiter.allow(count):
            raise RuntimeError("rate_limit_exceeded")

    def analyze(self, url: str, save: bool = False, db=None) -> URLAnalysisResult:
        validation = validate_url_format(url)
        domain = validation.domain
        normalized_url = validation.normalized_url
        issues: list[str] = []

        unwrapped_url = self.unwrap_shortened_url(normalized_url)
        parsed = urlparse(unwrapped_url)

        is_blacklisted = self._domain_matches_list(domain, self.blacklist)
        is_whitelisted = self._domain_matches_list(domain, self.whitelist)

        spam_score = self.calculate_spam_score(parsed)
        phishing_score = self.calculate_phishing_score(parsed, domain)
        malicious_score = self.calculate_malicious_score(parsed, domain)
        authenticity_score = self.calculate_authenticity_score(
            parsed, is_blacklisted, is_whitelisted
        )

        if detect_url_shorteners(domain):
            issues.append("shortener_detected")
        if self.detect_homograph_attack(domain):
            issues.append("homograph_suspected")
        if is_blacklisted:
            issues.append("blacklisted_domain")
        if not validation.is_valid:
            issues.append(validation.reason or "invalid_url")

        result = URLAnalysisResult(
            url=url,
            normalized_url=normalized_url,
            unwrapped_url=unwrapped_url,
            domain=domain,
            is_valid=validation.is_valid,
            reason=validation.reason,
            spam_score=spam_score,
            phishing_score=phishing_score,
            malicious_score=malicious_score,
            authenticity_score=authenticity_score,
            is_blacklisted=is_blacklisted,
            is_whitelisted=is_whitelisted,
            issues=issues,
        )

        if save and db:
            db.save_analysis(result)

        return result

    def analyze_text(
        self, text: str, save: bool = False, db=None
    ) -> list[URLAnalysisResult]:
        urls = extract_urls(text)
        if not urls:
            return []
        if len(urls) > 50:
            raise ValueError("batch_limit_exceeded")
        self.check_rate_limit(len(urls))
        return [self.analyze(url, save=save, db=db) for url in urls]

    def batch_analyze(
        self, urls: Iterable[str], save: bool = False, db=None
    ) -> list[URLAnalysisResult]:
        cleaned = normalize_inputs(urls)
        if len(cleaned) > 50:
            raise ValueError("batch_limit_exceeded")
        if cleaned:
            self.check_rate_limit(len(cleaned))
        return [self.analyze(url, save=save, db=db) for url in cleaned]

    def detect_homograph_attack(self, domain: str | None) -> bool:
        if not domain:
            return False
        if domain.startswith("xn--"):
            return True

        has_non_ascii = any(ord(ch) > 127 for ch in domain)
        if not has_non_ascii:
            return False

        scripts = {unicodedata.name(ch).split(" ")[0] for ch in domain if ord(ch) > 127}
        if len(scripts) > 1:
            return True

        confusables = {"ο", "е", "ѕ", "і", "ӏ", "а"}  # common lookalikes
        if any(ch in confusables for ch in domain):
            return True
        return False

    def calculate_spam_score(self, parsed) -> float:
        score = 0.1
        query = parse_qs(parsed.query)
        tracking_params = [k for k in query if k.startswith(("utm_", "ref", "clickid"))]
        score += min(len(tracking_params) * 0.1, 0.5)

        keyword_hits = sum(
            1 for kw in self.suspicious_keywords if kw in parsed.geturl().lower()
        )
        score += min(keyword_hits * 0.1, 0.4)

        redirect_params = [
            v for key in ("url", "u", "redirect", "target") for v in query.get(key, [])
        ]
        if any(v.startswith(("http", "https")) for v in redirect_params):
            score += 0.2

        if detect_url_shorteners(parsed.hostname or ""):
            score += 0.2

        return min(score, 1.0)

    def calculate_phishing_score(self, parsed, domain: str | None) -> float:
        score = 0.0
        if self.detect_homograph_attack(domain):
            score += 0.4

        lower_url = parsed.geturl().lower()
        keyword_hits = sum(1 for kw in PHISHING_KEYWORDS if kw in lower_url)
        score += min(keyword_hits * 0.15, 0.6)

        brand_words = {"paypal", "apple", "google", "microsoft", "bank", "secure"}
        if domain and any(brand in domain for brand in brand_words):
            score += 0.2
        return min(score, 1.0)

    def calculate_malicious_score(self, parsed, domain: str | None) -> float:
        score = 0.0
        path = parsed.path.lower()
        if any(path.endswith(ext) for ext in EXECUTABLE_EXTENSIONS):
            score += 0.5

        if parsed.port and parsed.port in SUSPICIOUS_PORTS:
            score += 0.2

        if domain and domain.replace(".", "").isdigit():
            score += 0.3

        encoded_count = parsed.geturl().count("%")
        if encoded_count > 5:
            score += 0.2

        return min(score, 1.0)

    def calculate_authenticity_score(
        self, parsed, is_blacklisted: bool, is_whitelisted: bool
    ) -> float:
        score = 0.5
        if parsed.scheme == "https":
            score += 0.2

        domain = parsed.hostname or ""
        if domain.split(".")[-1] in SUSPICIOUS_TLDS:
            score -= 0.2
        if len(domain) > 25:
            score -= 0.1

        if is_whitelisted:
            score += 0.2
        if is_blacklisted:
            score -= 0.3
        return min(max(score, 0.0), 1.0)

    def unwrap_shortened_url(self, url: str) -> str:
        parsed = urlparse(url)
        if not detect_url_shorteners(parsed.hostname or ""):
            return url
        query = parse_qs(parsed.query)
        for key in ("url", "u", "redirect", "target"):
            candidates = query.get(key, [])
            for candidate in candidates:
                decoded = unquote(candidate)
                if decoded.startswith(("http://", "https://")):
                    return decoded
        return url

    def _domain_matches_list(self, domain: str | None, domain_set: set[str]) -> bool:
        if not domain or not domain_set:
            return False
        domain = domain.lower()
        return any(domain == item or domain.endswith(f".{item}") for item in domain_set)


def detect_url_shorteners(domain: str | None) -> bool:
    if not domain:
        return False
    domain = domain.lower()
    return domain in SHORTENER_DOMAINS


def render_analysis_table(results: list[URLAnalysisResult]) -> None:
    table = Table(show_lines=False)
    table.add_column("URL", overflow="fold")
    table.add_column("Spam", justify="right")
    table.add_column("Phishing", justify="right")
    table.add_column("Malicious", justify="right")
    table.add_column("Authenticity", justify="right")
    table.add_column("Notes", overflow="fold")

    for result in results:
        notes = []
        if result.is_blacklisted:
            notes.append("[red]BLACKLISTED[/red]")
        if result.is_whitelisted:
            notes.append("[green]WHITELISTED[/green]")
        if result.issues:
            notes.extend(result.issues)

        table.add_row(
            result.url,
            f"{result.spam_score:.2f}",
            f"{result.phishing_score:.2f}",
            f"{result.malicious_score:.2f}",
            f"{result.authenticity_score:.2f}",
            ", ".join(notes) or "-",
        )

    console.print(table)
