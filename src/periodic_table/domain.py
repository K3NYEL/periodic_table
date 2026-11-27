"""Pure domain model. This module deliberately has no Flet dependency."""
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Element:
    number: int
    symbol: str
    name: str
    group: int
    period: int
    block: str
    category: str
    atomic_mass: float | None = None
    phase: str | None = None
    electronegativity: float | None = None
    melting_point: float | None = None
    boiling_point: float | None = None
    density: float | None = None
    density_unit: str | None = None
    source_url: str | None = None
    electron_configuration: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Element":
        allowed = cls.__dataclass_fields__
        return cls(**{key: value for key, value in data.items() if key in allowed})

    @property
    def position(self) -> tuple[int, int]:
        return self.period, self.group
