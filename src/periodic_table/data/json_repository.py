import json
from pathlib import Path
from typing import List, Optional
from ..domain.models.element import Element, Category, Phase
from ..domain.repositories import ElementRepository

class JsonElementRepository(ElementRepository):
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)
        self._elements: List[Element] = []
        self._load()

    def _load(self):
        with open(self.data_path) as f:
            data = json.load(f)
            for item in data:
                el = Element(
                    number=item["number"],
                    symbol=item["symbol"],
                    name=item["name"],
                    weight=item["weight"],
                    category=Category(item["category"]),
                    phase=Phase(item["phase"]),
                    electronegativity=item.get("electronegativity", 0),
                    melting_point=item.get("melting_point", 0),
                )
                self._elements.append(el)

    def get_all(self) -> List[Element]:
        return self._elements

    def get_by_number(self, number: int) -> Optional[Element]:
        for el in self._elements:
            if el.number == number:
                return el
        return None

    def search(self, query: str) -> List[Element]:
        query_lower = query.lower()
        return [
            el for el in self._elements
            if query_lower in el.name.lower() or 
               query_lower in el.symbol.lower() or 
               str(query_lower) == str(el.number)
        ]