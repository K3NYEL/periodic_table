"""Application services. No Flet imports are allowed in this module."""
import re
from dataclasses import dataclass
from .domain import Element
from .repository import ElementRepository


class ElementService:
    def __init__(self, repository: ElementRepository):
        self.repository = repository

    def all(self) -> list[Element]:
        return self.repository.all()

    def get(self, number: int) -> Element | None:
        return self.repository.get(number)

    def search(self, query: str) -> list[Element]:
        query = (query or "").strip().casefold()
        elements = self.all()
        if not query:
            return elements
        # Exact atomic number and common natural-language property queries.
        match = re.fullmatch(r"(?:z|número|numero)?\s*(>=|<=|>|<|=)\s*(\d+(?:\.\d+)?)", query)
        if match:
            operator, raw = match.groups()
            threshold = float(raw)
            compare = {
                ">": lambda n: n > threshold, ">=": lambda n: n >= threshold,
                "<": lambda n: n < threshold, "<=": lambda n: n <= threshold,
                "=": lambda n: n == threshold,
            }[operator]
            return [item for item in elements if compare(item.number)]
        if query in {"gas", "gases"}:
            return [item for item in elements if item.phase == "Gas"]
        if query in {"líquido", "liquido", "liquids"}:
            return [item for item in elements if item.phase == "Líquido"]
        if query in {"sólido", "solido", "solids"}:
            return [item for item in elements if item.phase == "Sólido"]
        if query.startswith("grupo "):
            try:
                group = int(query.split()[-1])
                return [item for item in elements if item.group == group]
            except ValueError:
                pass
        if query.startswith("período ") or query.startswith("periodo "):
            try:
                period = int(query.split()[-1])
                return [item for item in elements if item.period == period]
            except ValueError:
                pass
        return [
            item for item in elements
            if query in item.name.casefold()
            or query == item.symbol.casefold()
            or query == str(item.number)
            or query in item.category.casefold()
            or query in (item.electron_configuration or "").casefold()
        ]

    def filter(self, items, category=None, phase=None, block=None, period=None):
        return [
            item for item in items
            if (not category or item.category == category)
            and (not phase or item.phase == phase)
            and (not block or item.block == block)
            and (not period or item.period == period)
        ]


@dataclass(frozen=True, slots=True)
class ComparisonDifference:
    label: str
    element: Element | None
    value: float | None


class CompareService:
    LIMIT = 4
    NUMERIC_PROPERTIES = {
        "Masa atómica": "atomic_mass",
        "Electronegatividad": "electronegativity",
        "Punto de fusión": "melting_point",
        "Punto de ebullición": "boiling_point",
        "Densidad": "density",
    }

    def __init__(self):
        self._numbers: list[int] = []

    @property
    def numbers(self) -> list[int]:
        return list(self._numbers)

    def add(self, number: int) -> bool:
        number = int(number)
        if number in self._numbers:
            return True
        if len(self._numbers) >= self.LIMIT:
            return False
        self._numbers.append(number)
        return True

    def remove(self, number: int) -> bool:
        if number not in self._numbers:
            return False
        self._numbers.remove(number)
        return True

    def toggle(self, number: int) -> bool:
        return self.remove(number) if number in self._numbers else self.add(number)

    def clear(self) -> None:
        self._numbers.clear()

    def extremes(self, elements: list[Element]) -> dict[str, tuple[Element, float]]:
        result = {}
        for label, attribute in self.NUMERIC_PROPERTIES.items():
            available = [(item, getattr(item, attribute)) for item in elements]
            available = [(item, value) for item, value in available if value is not None]
            if available:
                result[label] = max(available, key=lambda pair: pair[1])
        return result
