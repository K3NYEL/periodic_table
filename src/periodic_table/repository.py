"""Data layer: repository contract and JSON implementation."""
import json
from pathlib import Path
from typing import Protocol, runtime_checkable

from .domain import Element


@runtime_checkable
class ElementRepository(Protocol):
    def all(self) -> list[Element]: ...
    def get(self, number: int) -> Element | None: ...
    def reload(self) -> int: ...


class JsonElementRepository:
    def __init__(self, path: Path | None = None):
        self.path = path or Path(__file__).resolve().parents[1] / "data" / "elements.json"
        self._elements: tuple[Element, ...] = ()
        self._by_number: dict[int, Element] = {}
        self.reload()

    def reload(self) -> int:
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise FileNotFoundError(f"No se encontró el archivo de elementos: {self.path}") from exc
        if not isinstance(payload, list):
            raise ValueError("El archivo de elementos debe contener una lista JSON.")
        elements = tuple(Element.from_dict(item) for item in payload)
        numbers = [item.number for item in elements]
        if len(numbers) != len(set(numbers)):
            raise ValueError("Hay números atómicos duplicados en elements.json.")
        if sorted(numbers) != list(range(1, 119)):
            raise ValueError("El conjunto de datos debe contener exactamente los elementos 1–118.")
        if any(not item.symbol or not item.name for item in elements):
            raise ValueError("Cada elemento necesita nombre y símbolo.")
        self._elements = tuple(sorted(elements, key=lambda item: item.number))
        self._by_number = {item.number: item for item in self._elements}
        return len(self._elements)

    def all(self) -> list[Element]:
        return list(self._elements)

    def get(self, number: int) -> Element | None:
        return self._by_number.get(int(number))
