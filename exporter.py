"""CSV and JSON export functionality."""
from __future__ import annotations
import csv
import json
from pathlib import Path
from typing import Iterable
from .models import Record

class DataExporter:
    def _rows(self, records: Iterable[Record]) -> list[dict]:
        return [r.to_dict() for r in records]

    def to_json(self, records: Iterable[Record], path: str | Path) -> Path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(self._rows(records), indent=2, ensure_ascii=False), encoding="utf-8")
        return target

    def to_csv(self, records: Iterable[Record], path: str | Path) -> Path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        rows = self._rows(records)
        with target.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(
                fh, fieldnames=["title", "price", "rating", "availability", "source_url"]
            )
            writer.writeheader()
            writer.writerows(rows)
        return target

    def from_json(self, path: str | Path) -> list[Record]:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return [Record(**item) for item in data]
