"""SQLite persistence for attempts and local settings."""
from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator


DEFAULT_SETTINGS: dict[str, Any] = {
    "questions_per_quiz": 10, "timer_enabled": True, "timer_seconds": 20,
    "dark_mode": False, "sound_enabled": False,
}


class Database:
    def __init__(self, path: str | Path | None = None) -> None:
        self.path = Path(path) if path else Path.home() / ".python_quiz_master.sqlite3"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def initialize(self) -> None:
        with self.connect() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT, player_name TEXT NOT NULL,
                category TEXT NOT NULL, difficulty TEXT NOT NULL, total INTEGER NOT NULL,
                correct INTEGER NOT NULL, incorrect INTEGER NOT NULL, unanswered INTEGER NOT NULL,
                score INTEGER NOT NULL, percentage REAL NOT NULL, duration_seconds INTEGER NOT NULL,
                played_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, review_json TEXT NOT NULL DEFAULT '[]'
            )""")
            conn.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
            for key, value in DEFAULT_SETTINGS.items():
                conn.execute("INSERT OR IGNORE INTO settings(key, value) VALUES (?, ?)",
                             (key, json.dumps(value)))

    def save_result(self, player_name: str, category: str, difficulty: str,
                    summary: Any, review: list[dict[str, Any]]) -> int:
        with self.connect() as conn:
            cursor = conn.execute("""INSERT INTO results
                (player_name, category, difficulty, total, correct, incorrect, unanswered,
                 score, percentage, duration_seconds, review_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (player_name, category, difficulty, summary.total, summary.correct,
                 summary.incorrect, summary.unanswered, summary.score, summary.percentage,
                 summary.duration_seconds, json.dumps(review, ensure_ascii=False)))
            return int(cursor.lastrowid)

    def get_results(self, limit: int = 500) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute("SELECT * FROM results ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [dict(row) for row in rows]

    def get_result(self, result_id: int) -> dict[str, Any] | None:
        with self.connect() as conn:
            row = conn.execute("SELECT * FROM results WHERE id = ?", (result_id,)).fetchone()
        return dict(row) if row else None

    def clear_results(self) -> None:
        with self.connect() as conn:
            conn.execute("DELETE FROM results")

    def get_settings(self) -> dict[str, Any]:
        settings = DEFAULT_SETTINGS.copy()
        with self.connect() as conn:
            rows = conn.execute("SELECT key, value FROM settings").fetchall()
        for row in rows:
            try:
                if row["key"] in settings:
                    settings[row["key"]] = json.loads(row["value"])
            except (ValueError, TypeError):
                pass
        return settings

    def save_settings(self, settings: dict[str, Any]) -> None:
        with self.connect() as conn:
            for key, value in settings.items():
                if key in DEFAULT_SETTINGS:
                    conn.execute("INSERT INTO settings(key, value) VALUES (?, ?) "
                                 "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                                 (key, json.dumps(value)))
