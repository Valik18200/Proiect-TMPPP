# strategy.py
from abc import ABC, abstractmethod


class SortStrategy(ABC):
    @abstractmethod
    def sort(self, sauces: list) -> list:
        pass

    @abstractmethod
    def name(self) -> str:
        pass


class SortByPrice(SortStrategy):
    def sort(self, sauces: list) -> list:
        return sorted(sauces, key=lambda s: s["price"])

    def name(self) -> str:
        return "Pret (crescator)"


class SortByPriceDesc(SortStrategy):
    def sort(self, sauces: list) -> list:
        return sorted(sauces, key=lambda s: s["price"], reverse=True)

    def name(self) -> str:
        return "Pret (descrescator)"


class SortByName(SortStrategy):
    def sort(self, sauces: list) -> list:
        return sorted(sauces, key=lambda s: s["name"])

    def name(self) -> str:
        return "Nume (A-Z)"


class SortByScoville(SortStrategy):
    def sort(self, sauces: list) -> list:
        return sorted(sauces, key=lambda s: s["scoville"])

    def name(self) -> str:
        return "Scoville (crescator)"


class SortByScovilleDesc(SortStrategy):
    def sort(self, sauces: list) -> list:
        return sorted(sauces, key=lambda s: s["scoville"], reverse=True)

    def name(self) -> str:
        return "Scoville (descrescator - cel mai iute)"


class SauceCatalog:
    def __init__(self):
        self._sauces = []
        self._strategy = SortByName()

    def add_sauce(self, name: str, price: float, scoville: int):
        self._sauces.append({"name": name, "price": price, "scoville": scoville})

    def set_sort_strategy(self, strategy: SortStrategy):
        self._strategy = strategy

    def get_sorted(self) -> list:
        return self._strategy.sort(self._sauces)

    def display(self) -> str:
        lines = [f"  Sortare: {self._strategy.name()}"]
        for sauce in self.get_sorted():
            lines.append(f"    {sauce['name']} - {sauce['price']:.2f} LEI (Scoville: {sauce['scoville']:,} SHU)")
        return "\n".join(lines)