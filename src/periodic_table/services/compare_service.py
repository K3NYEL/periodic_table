class CompareService:
    LIMIT = 4

    def __init__(self):
        self.numbers: list[int] = []

    def toggle(self, number: int) -> bool:
        if number in self.numbers:
            self.numbers.remove(number)
            return True
        if len(self.numbers) >= self.LIMIT:
            return False
        self.numbers.append(number)
        return True

    def clear(self) -> None:
        self.numbers.clear()
