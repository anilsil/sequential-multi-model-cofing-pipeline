from __future__ import annotations

import re
from typing import Iterable

URL_REGEX = re.compile(
    r"\b((?:(?:https?|ftp)://)?(?:www\.)?[a-z0-9][\w\-.]*\.[a-z]{2,}"
    r"(?::\d{2,5})?(?:/[^\s<>()\[\]{}]*)?)",
    re.IGNORECASE,
)


def _strip_trailing_punctuation(url: str) -> str:
    return url.rstrip(".,;:!?)]}>\"'")


def extract_urls(text: str | None) -> list[str]:
    """
    Extract URLs from arbitrary text (plain, markdown, HTML-like).

    Uses a compiled regex for performance and strips trailing punctuation
    that often follows inline URLs.
    """
    if not text:
        return []

    seen: set[str] = set()
    results: list[str] = []

    for match in URL_REGEX.finditer(text):
        full = match.group(0)
        url = full if full.startswith(("http://", "https://", "ftp://")) else f"http://{full}"
        cleaned = _strip_trailing_punctuation(url)
        if cleaned not in seen:
            seen.add(cleaned)
            results.append(cleaned)

    return results


def normalize_inputs(urls: Iterable[str | None]) -> list[str]:
    return [url for url in (u.strip() for u in urls if u) if url]
