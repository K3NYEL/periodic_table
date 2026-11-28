from abc import ABC, abstractmethod
from typing import Optional

from .models.element import Element


class ElementRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Element]:
        raise NotImplementedError

    @abstractmethod
    def get_by_number(self, number: int) -> Optional[Element]:
        raise NotImplementedError

    @abstractmethod
    def search(self, query: str) -> list[Element]:
        raise NotImplementedError
