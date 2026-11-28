from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Category(str, Enum):
    NONMETAL = "nonmetal"
    NOBLE_GAS = "noble_gas"
    ALKALI_METAL = "alkali_metal"
    ALKALINE_EARTH = "alkaline_earth"
    METALLOID = "metalloid"
    HALOGEN = "halogen"
    POST_TRANSITION = "post_transition"
    TRANSITION = "transition"
    LANTHANIDE = "lanthanide"
    ACTINIDE = "actinide"
    UNKNOWN = "unknown"


class Phase(str, Enum):
    SOLID = "solid"
    LIQUID = "liquid"
    GAS = "gas"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class Element:
    number: int
    symbol: str
    name: str
    group: Optional[int]
    period: int
    block: str
    category: Category
    atomic_mass: Optional[float]
    phase: Phase
    electronegativity: Optional[float] = None
    melting_point: Optional[float] = None
    boiling_point: Optional[float] = None
    density: Optional[float] = None
    electron_configuration: Optional[str] = None
    density_unit: Optional[str] = None
    source_url: Optional[str] = None

    @property
    def weight(self) -> Optional[float]:
        """Compatibility alias for older code."""
        return self.atomic_mass
