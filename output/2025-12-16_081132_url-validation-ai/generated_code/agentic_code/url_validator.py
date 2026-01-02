from __future__ import annotations

import ipaddress
import re
from dataclasses import dataclass
from urllib.parse import urlparse

MAX_URL_LENGTH = 2000
ALLOWED_SCHEMES = {"http", "https"}
SUSPICIOUS_SCHEMES = {"javascript", "data", "file", "vbscript"}
DOMAIN_REGEX = re.compile(r"^(?=.{1,253}$)([A-Za-z0-9\u00a1-\uffff-]{1,63}\.)+[A-Za-z\u00a1-\uffff]{2,}$")
PORT_REGEX = re.compile(r":(\d+)$")


@dataclass
class URLValidationResult:
    original_url: str
    normalized_url: str
    domain: str | None
    is_valid: bool
    reason: str | None = None


def _looks_like_ip(host: str) -> bool:
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def _clean_url(url: str) -> str:
    trimmed = url.strip().replace("\\", "/")
    if trimmed.startswith("//"):
        return f"http:{trimmed}"
    if not trimmed.startswith(("http://", "https://")):
        return f"http://{trimmed}"
    return trimmed


def _extract_domain(netloc: str) -> str | None:
    if not netloc:
        return None
    host = netloc.split("@")[-1]
    if ":" in host:
        host = host.split(":", maxsplit=1)[0]
    return host.lower()


def _valid_domain(host: str) -> bool:
    if _looks_like_ip(host):
        return True
    if host.startswith(".") or host.endswith("."):
        return False
    if "_" in host:
        return False
    return bool(DOMAIN_REGEX.match(host)) or host == "localhost"


def validate_url_format(url: str) -> URLValidationResult:
    if not url or len(url) > MAX_URL_LENGTH:
        return URLValidationResult(url, url, None, False, "empty_or_too_long")

    raw = url.strip()
    if "://" in raw:
        scheme_candidate = raw.split("://", maxsplit=1)[0].lower()
        if scheme_candidate in SUSPICIOUS_SCHEMES:
            return URLValidationResult(url, raw, None, False, "disallowed_scheme")
        if scheme_candidate not in ALLOWED_SCHEMES:
            return URLValidationResult(url, raw, None, False, "invalid_scheme")
    elif ":" in raw:
        scheme_candidate = raw.split(":", maxsplit=1)[0].lower()
        if scheme_candidate in SUSPICIOUS_SCHEMES:
            return URLValidationResult(url, raw, None, False, "disallowed_scheme")

    cleaned = _clean_url(raw)
    parsed = urlparse(cleaned)

    if parsed.scheme.lower() in SUSPICIOUS_SCHEMES:
        return URLValidationResult(url, cleaned, None, False, "disallowed_scheme")

    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        return URLValidationResult(url, cleaned, None, False, "invalid_scheme")

    domain = _extract_domain(parsed.netloc)
    if not domain or not _valid_domain(domain):
        return URLValidationResult(url, cleaned, domain, False, "invalid_domain")

    if PORT_REGEX.search(parsed.netloc):
        port = int(PORT_REGEX.search(parsed.netloc).group(1))
        if port <= 0 or port > 65535:
            return URLValidationResult(url, cleaned, domain, False, "invalid_port")

    return URLValidationResult(url, cleaned, domain, True, None)
