from dataclasses import dataclass, field
from typing import Optional

from ..domain.models.element import Element


@dataclass
class AppState:
    query: str = ""
    selected_element: Optional[Element] = None
    current_view: str = "/"
    compare_numbers: list[int] = field(default_factory=list)

    def select(self, element: Optional[Element]) -> None:
        self.selected_element = element

    def set_query(self, query: str) -> None:
        self.query = query
