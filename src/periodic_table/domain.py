"""Pure domain types; intentionally independent from Flet."""
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True, slots=True)
class Element:
    number: int
    symbol: str
    name: str
    group: int
    period: int
    block: str
    category: str
    atomic_mass: Optional[float] = None
    phase: Optional[str] = None
    electronegativity: Optional[float] = None
    melting_point: Optional[float] = None
    boiling_point: Optional[float] = None
    density: Optional[float] = None
    electron_configuration: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
