"""Domain models using OOP."""
from dataclasses import dataclass, asdict
from typing import Any

@dataclass
class Record:
    title: str
    price: str = ""
    rating: str = ""
    availability: str = ""
    source_url: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

class BaseProcessor:
    """Base class demonstrating encapsulation/inheritance."""
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def process(self, value: Any) -> Any:
        raise NotImplementedError

class RecordProcessor(BaseProcessor):
    """Concrete processor for scraped records."""
    def process(self, value: Record) -> Record:
        return value
