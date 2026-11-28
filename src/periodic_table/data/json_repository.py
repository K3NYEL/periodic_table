import json
from pathlib import Path
from typing import Optional

from ..domain.models.element import Category, Element, Phase
from ..domain.repositories import ElementRepository


_CATEGORY_ALIASES = {
    "not metal": Category.NONMETAL,
    "nonmetal": Category.NONMETAL,
    "noble gas": Category.NOBLE_GAS,
    "alkaline": Category.ALKALI_METAL,
    "alkali metal": Category.ALKALI_METAL,
    "alkaline earth": Category.ALKALINE_EARTH,
    "metalloid": Category.METALLOID,
    "halogen": Category.HALOGEN,
    "halógeno": Category.HALOGEN,
    "post-transition": Category.POST_TRANSITION,
    "post transition": Category.POST_TRANSITION,
    "transition": Category.TRANSITION,
    "lanthanide": Category.LANTHANIDE,
    "lantánido": Category.LANTHANIDE,
    "actinide": Category.ACTINIDE,
}

_PHASE_ALIASES = {
    "solid": Phase.SOLID,
    "sólido": Phase.SOLID,
    "líquido": Phase.LIQUID,
    "liquid": Phase.LIQUID,
    "gas": Phase.GAS,
}


def _optional_float(value):
    return None if value is None else float(value)


class JsonElementRepository(ElementRepository):
    def __init__(self, data_path: Optional[str | Path] = None):
        project_root = Path(__file__).resolve().parents[3]
        self.data_path = Path(data_path) if data_path else project_root / "assets" / "data" / "elements.json"
        if not self.data_path.is_absolute():
            self.data_path = project_root / self.data_path
        self._elements = self._load()

    @staticmethod
    def _parse(item: dict) -> Element:
        raw_category = str(item.get("category", "")).strip().casefold()
        raw_phase = str(item.get("phase", "")).strip().casefold()
        try:
            category = _CATEGORY_ALIASES[raw_category]
        except KeyError as exc:
            raise ValueError(f"Unknown category {item.get('category')!r} for element {item.get('number')}") from exc
        phase = _PHASE_ALIASES.get(raw_phase, Phase.UNKNOWN)
        return Element(
            number=int(item["number"]),
            symbol=str(item["symbol"]).strip(),
            name=str(item["name"]).strip(),
            group=int(item["group"]) if item.get("group") is not None else None,
            period=int(item["period"]),
            block=str(item.get("block", "")).strip(),
            category=category,
            atomic_mass=_optional_float(item.get("atomic_mass", item.get("weight"))),
            phase=phase,
            electronegativity=_optional_float(item.get("electronegativity")),
            melting_point=_optional_float(item.get("melting_point")),
            boiling_point=_optional_float(item.get("boiling_point")),
            density=_optional_float(item.get("density")),
            electron_configuration=item.get("electron_configuration"),
            density_unit=item.get("density_unit"),
            source_url=item.get("source_url"),
        )

    def _load(self) -> list[Element]:
        if not self.data_path.is_file():
            raise FileNotFoundError(f"Element data file not found: {self.data_path}")
        with self.data_path.open("r", encoding="utf-8") as file:
            raw_data = json.load(file)
        if not isinstance(raw_data, list):
            raise ValueError("Element data must be a JSON array")
        elements = [self._parse(item) for item in raw_data]
        numbers = [element.number for element in elements]
        if len(numbers) != len(set(numbers)):
            raise ValueError("Element data contains duplicate atomic numbers")
        return sorted(elements, key=lambda element: element.number)

    def get_all(self) -> list[Element]:
        return list(self._elements)

    def get_by_number(self, number: int) -> Optional[Element]:
        return next((element for element in self._elements if element.number == number), None)

    def search(self, query: str) -> list[Element]:
        term = query.strip().casefold()
        if not term:
            return self.get_all()
        return [
            element for element in self._elements
            if term in element.name.casefold()
            or term in element.symbol.casefold()
            or term == str(element.number)
        ]
