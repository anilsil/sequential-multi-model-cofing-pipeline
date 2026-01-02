from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Iterable

from .url_analyzer import URLAnalysisResult, DEFAULT_DB_PATH


class URLAnalysisDB:
    def __init__(self, db_path: Path | None = None):
        self.db_path = db_path or DEFAULT_DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_table()

    def _ensure_table(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS url_analysis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT,
                    normalized_url TEXT,
                    unwrapped_url TEXT,
                    domain TEXT,
                    spam_score REAL,
                    phishing_score REAL,
                    malicious_score REAL,
                    authenticity_score REAL,
                    is_blacklisted INTEGER,
                    is_whitelisted INTEGER,
                    issues TEXT,
                    timestamp REAL
                )
                """
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_url_domain ON url_analysis(domain)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_url_timestamp ON url_analysis(timestamp)")
            conn.commit()

    def save_analysis(self, result: URLAnalysisResult) -> None:
        payload = (
            result.url,
            result.normalized_url,
            result.unwrapped_url,
            result.domain,
            result.spam_score,
            result.phishing_score,
            result.malicious_score,
            result.authenticity_score,
            int(result.is_blacklisted),
            int(result.is_whitelisted),
            json.dumps(result.issues),
            result.timestamp,
        )
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO url_analysis (
                    url, normalized_url, unwrapped_url, domain,
                    spam_score, phishing_score, malicious_score,
                    authenticity_score, is_blacklisted, is_whitelisted,
                    issues, timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                payload,
            )
            conn.commit()

    def fetch_recent(self, limit: int = 50) -> list[dict]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                """
                SELECT url, normalized_url, unwrapped_url, domain,
                       spam_score, phishing_score, malicious_score,
                       authenticity_score, is_blacklisted, is_whitelisted,
                       issues, timestamp
                FROM url_analysis
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        results = []
        for row in rows:
            results.append(
                {
                    "url": row[0],
                    "normalized_url": row[1],
                    "unwrapped_url": row[2],
                    "domain": row[3],
                    "spam_score": row[4],
                    "phishing_score": row[5],
                    "malicious_score": row[6],
                    "authenticity_score": row[7],
                    "is_blacklisted": bool(row[8]),
                    "is_whitelisted": bool(row[9]),
                    "issues": json.loads(row[10] or "[]"),
                    "timestamp": row[11],
                }
            )
        return results

    def bulk_save(self, results: Iterable[URLAnalysisResult]) -> None:
        for result in results:
            self.save_analysis(result)
