from abc import ABC, abstractmethod
from typing import List, Optional
from .models.element import Element

class ElementRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Element]: ...
    
    @abstractmethod
    def get_by_number(self, number: int) -> Optional[Element]: ...
    
    @abstractmethod
    def search(self, query: str) -> List[Element]: ...