from dataclasses import dataclass
from enum import Enum

class Category(Enum):
    METAL = "Metal"
    NONMETAL = "Nonmetal"
    METALLOID = "Metalloid"
    NOBLE_GAS = "Noble Gas"
    # ... add others

class Phase(Enum):
    SOLID = "Solid"
    LIQUID = "Liquid"
    GAS = "Gas"

@dataclass
class Element:
    number: int
    symbol: str
    name: str
    weight: float
    category: Category
    phase: Phase
    electronegativity: float
    melting_point: float
    # ... other properties