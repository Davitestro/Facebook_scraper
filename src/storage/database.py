"""Database persistence utilities backed by SQLite."""

import json
import sqlite3
from typing import Any, Optional


class DatabaseStorage:
    """Store scraped payloads in a SQLite database."""

    def __init__(self, connection: Optional[Any] = None, table_name: str = "scraped_items"):
        self.connection = connection
        self.table_name = table_name
        self._ensure_connection()
        self._ensure_table()

    def _ensure_connection(self) -> None:
        if self.connection is None:
            self.connection = sqlite3.connect(":memory:")
        elif isinstance(self.connection, str):
            self.connection = sqlite3.connect(self.connection)

    def _ensure_table(self) -> None:
        self.connection.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.connection.commit()

    def save(self, data: Any) -> int:
        payload = json.dumps(data)
        cursor = self.connection.execute(
            f"INSERT INTO {self.table_name} (payload) VALUES (?)",
            (payload,),
        )
        self.connection.commit()
        return int(cursor.lastrowid)

    def load(self, limit: Optional[int] = None) -> list[dict[str, Any]]:
        query = f"SELECT payload FROM {self.table_name} ORDER BY id DESC"
        if limit is not None:
            query += f" LIMIT {limit}"

        rows = self.connection.execute(query).fetchall()
        return [json.loads(row[0]) for row in rows]

    def delete_all(self) -> None:
        self.connection.execute(f"DELETE FROM {self.table_name}")
        self.connection.commit()

    def close(self) -> None:
        if self.connection is not None and hasattr(self.connection, "close"):
            self.connection.close()
            self.connection = None
