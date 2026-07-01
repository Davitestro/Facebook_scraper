"""CSV storage helpers for exporting scraped data."""

import csv
import os
from typing import Any, Dict, Iterable, List, Optional


class CSVStorage:
    """Persist rows to a CSV file."""

    def __init__(self, filepath: str, fieldnames: Optional[List[str]] = None, connection: Any = None):
        self.filepath = filepath
        self.fieldnames = fieldnames
        self.connection = connection
        self._ensure_directory()

    def _ensure_directory(self) -> None:
        directory = os.path.dirname(self.filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def save(self, rows: Iterable[Dict[str, Any]], fieldnames: Optional[List[str]] = None) -> None:
        resolved_fieldnames = fieldnames or self.fieldnames
        with open(self.filepath, "w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=resolved_fieldnames or [])
            if resolved_fieldnames:
                writer.writeheader()
            for row in rows:
                writer.writerow(row)

    def load(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.filepath):
            return []

        with open(self.filepath, "r", encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))
