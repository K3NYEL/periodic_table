"""Application use-cases, independent of the UI toolkit."""
from .repository import ElementRepository

class ElementService:
    def __init__(self, repository: ElementRepository): self.repository = repository
    def all(self): return self.repository.all()
    def get(self, number): return self.repository.get(number)
    def search(self, query: str):
        q=query.strip().casefold()
        if not q: return self.all()
        out=[]
        for e in self.all():
            if q in e.name.casefold() or q in e.symbol.casefold() or q == str(e.number): out.append(e)
        return out
    def filter(self, items, category=None, phase=None, block=None, period=None):
        return [e for e in items if (not category or e.category==category) and (not phase or e.phase==phase) and (not block or e.block==block) and (not period or e.period==period)]

class CompareService:
    LIMIT=4
    def __init__(self): self._numbers=[]
    @property
    def numbers(self): return list(self._numbers)
    def toggle(self, number):
        if number in self._numbers: self._numbers.remove(number); return True
        if len(self._numbers)>=self.LIMIT: return False
        self._numbers.append(number); return True
    def clear(self): self._numbers.clear()
