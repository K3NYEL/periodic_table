"""JSON data adapter and repository contract."""
import json
from pathlib import Path
from typing import Protocol
from .domain import Element

class ElementRepository(Protocol):
    def all(self) -> list[Element]: ...
    def get(self, number: int) -> Element | None: ...

class JsonElementRepository:
    def __init__(self, path: Path | None = None):
        self.path = path or Path(__file__).resolve().parents[1] / "data" / "elements.json"
        self._elements: list[Element] = []
        self.reload()

    def reload(self) -> int:
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        self._elements = [Element.from_dict(item) for item in raw]
        return len(self._elements)

    def all(self) -> list[Element]:
        return list(self._elements)

    def get(self, number: int) -> Element | None:
        return next((e for e in self._elements if e.number == number), None)
