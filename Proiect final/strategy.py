"""
STRATEGY — Algoritmi interschimbabili de sortare/filtrare a produselor
si de calcul al pretului final.
"""
from abc import ABC, abstractmethod
from typing import List


# ─────────────────────────────────────────
#  STRATEGIE: Sortare catalog
# ─────────────────────────────────────────

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, products: List[dict]) -> List[dict]:
        pass


class SortByPriceAsc(SortStrategy):
    def sort(self, products: List[dict]) -> List[dict]:
        return sorted(products, key=lambda p: p["price"])


class SortByPriceDesc(SortStrategy):
    def sort(self, products: List[dict]) -> List[dict]:
        return sorted(products, key=lambda p: p["price"], reverse=True)


class SortByScovilleAsc(SortStrategy):
    """De la cel mai bland la cel mai iute."""
    def sort(self, products: List[dict]) -> List[dict]:
        return sorted(products, key=lambda p: p["scoville"])


class SortByScovilleDesc(SortStrategy):
    """De la cel mai iute la cel mai bland."""
    def sort(self, products: List[dict]) -> List[dict]:
        return sorted(products, key=lambda p: p["scoville"], reverse=True)


class SortByName(SortStrategy):
    def sort(self, products: List[dict]) -> List[dict]:
        return sorted(products, key=lambda p: p["name"].lower())


# ─────────────────────────────────────────
#  STRATEGIE: Calcul discount
# ─────────────────────────────────────────

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, price: float, quantity: int) -> float:
        pass

    @abstractmethod
    def description(self) -> str:
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, price: float, quantity: int) -> float:
        return price * quantity

    def description(self) -> str:
        return "Fara reducere"


class BulkDiscount(DiscountStrategy):
    """10% reducere la 5+ bucati."""
    def apply(self, price: float, quantity: int) -> float:
        total = price * quantity
        return total * 0.90 if quantity >= 5 else total

    def description(self) -> str:
        return "Bulk -10% (minim 5 buc)"


class SeasonalDiscount(DiscountStrategy):
    """20% reducere sezoniera."""
    def apply(self, price: float, quantity: int) -> float:
        return price * quantity * 0.80

    def description(self) -> str:
        return "Sezonier -20%"


class LoyaltyDiscount(DiscountStrategy):
    """15% pentru clienti fideli."""
    def apply(self, price: float, quantity: int) -> float:
        return price * quantity * 0.85

    def description(self) -> str:
        return "Fidelitate -15%"


# ─────────────────────────────────────────
'  CONTEXT'
# ─────────────────────────────────────────

class SpiceCatalog:
    def __init__(self, products: List[dict]):
        self._products = products
        self._sort_strategy: SortStrategy = SortByName()
        self._discount_strategy: DiscountStrategy = NoDiscount()

    def set_sort_strategy(self, strategy: SortStrategy):
        self._sort_strategy = strategy

    def set_discount_strategy(self, strategy: DiscountStrategy):
        self._discount_strategy = strategy

    def get_sorted(self) -> List[dict]:
        return self._sort_strategy.sort(self._products)

    def calculate_total(self, product_name: str, quantity: int) -> float:
        for p in self._products:
            if p["name"] == product_name:
                return self._discount_strategy.apply(p["price"], quantity)
        return 0.0

    def get_discount_info(self) -> str:
        return self._discount_strategy.description()
