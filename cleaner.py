"""Text cleaning utilities using regular expressions."""
from __future__ import annotations
import re
from .logger import timed
from .models import Record

class TextCleaner:
    """Clean whitespace and unsafe control characters."""
    @staticmethod
    def clean_text(value: str) -> str:
        value = re.sub(r"\s+", " ", value or "")
        value = re.sub(r"[^\x20-\x7E₹€£$.,:/()'\"!?&%+\-]", "", value)
        return value.strip()

    @timed
    def clean_records(self, records: list[Record]) -> list[Record]:
        cleaned = []
        for r in records:
            cleaned.append(
                Record(
                    title=self.clean_text(r.title),
                    price=self.clean_text(r.price),
                    rating=self.clean_text(r.rating),
                    availability=self.clean_text(r.availability),
                    source_url=self.clean_text(r.source_url),
                )
            )
        return cleaned
