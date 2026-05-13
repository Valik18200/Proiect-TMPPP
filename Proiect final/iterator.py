"""
ITERATOR — Parcurgere uniforma a catalogului dupa diferite criterii,
fara a expune structura interna a colectiei.
"""
from abc import ABC, abstractmethod
from typing import List


class SpiceIterator(ABC):
    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def next(self) -> dict:
        pass

    @abstractmethod
    def reset(self):
        pass


# ─────────────────────────────────────────
'  ITERATORI CONCRETI'
# ─────────────────────────────────────────

class AllProductsIterator(SpiceIterator):
    """Parcurge toate produsele in ordinea adaugarii."""
    def __init__(self, products: List[dict]):
        self._products = products
        self._index    = 0

    def has_next(self) -> bool:
        return self._index < len(self._products)

    def next(self) -> dict:
        item = self._products[self._index]
        self._index += 1
        return item

    def reset(self):
        self._index = 0


class CategoryIterator(SpiceIterator):
    """Parcurge doar produsele dintr-o categorie specifica."""
    def __init__(self, products: List[dict], category: str):
        self._products = [p for p in products
                          if p.get("category", "").lower() == category.lower()]
        self._index    = 0

    def has_next(self) -> bool:
        return self._index < len(self._products)

    def next(self) -> dict:
        item = self._products[self._index]
        self._index += 1
        return item

    def reset(self):
        self._index = 0


class HeatRangeIterator(SpiceIterator):
    """Parcurge produsele intre o iuteala minima si maxima (SHU)."""
    def __init__(self, products: List[dict], min_shu: int, max_shu: int):
        self._products = [p for p in products
                          if min_shu <= p.get("scoville", 0) <= max_shu]
        self._index    = 0

    def has_next(self) -> bool:
        return self._index < len(self._products)

    def next(self) -> dict:
        item = self._products[self._index]
        self._index += 1
        return item

    def reset(self):
        self._index = 0


class PriceBudgetIterator(SpiceIterator):
    """Parcurge produsele sub un anumit pret maxim."""
    def __init__(self, products: List[dict], max_price: float):
        self._products = [p for p in products
                          if p.get("price", 0) <= max_price]
        self._index    = 0

    def has_next(self) -> bool:
        return self._index < len(self._products)

    def next(self) -> dict:
        item = self._products[self._index]
        self._index += 1
        return item

    def reset(self):
        self._index = 0


# ─────────────────────────────────────────
'  COLECTIE ITERABILA'
# ─────────────────────────────────────────

class SpiceCatalogCollection:
    def __init__(self):
        self._products: List[dict] = [
            {"name": "Sriracha Original",      "price": 39.99, "scoville": 2_200,     "category": "sos_iute"},
            {"name": "Habanero Mango Blast",   "price": 54.99, "scoville": 8_000,     "category": "sos_iute"},
            {"name": "Ghost Pepper Inferno",   "price": 69.99, "scoville": 100_000,   "category": "sos_iute"},
            {"name": "Sweet Chili Citric",     "price": 34.99, "scoville": 1_500,     "category": "sos_iute"},
            {"name": "Cayenne Pudra",          "price": 24.99, "scoville": 40_000,    "category": "condiment"},
            {"name": "Amestec Cajun",          "price": 29.99, "scoville": 5_000,     "category": "condiment"},
            {"name": "Fulgi Ardei Rosu",       "price": 19.99, "scoville": 30_000,    "category": "condiment"},
            {"name": "Jalapeno Intreg",        "price": 27.99, "scoville": 8_000,     "category": "ardei_deshidratat"},
            {"name": "Carolina Reaper Pudra",  "price": 79.99, "scoville": 2_200_000, "category": "ardei_deshidratat"},
            {"name": "Sare Roz cu Chili",      "price": 18.99, "scoville": 5_000,     "category": "sare_iute"},
            {"name": "Sare Neagra Ghost",      "price": 26.99, "scoville": 80_000,    "category": "sare_iute"},
        ]

    def all_iterator(self) -> AllProductsIterator:
        return AllProductsIterator(self._products)

    def category_iterator(self, category: str) -> CategoryIterator:
        return CategoryIterator(self._products, category)

    def heat_range_iterator(self, min_shu: int, max_shu: int) -> HeatRangeIterator:
        return HeatRangeIterator(self._products, min_shu, max_shu)

    def budget_iterator(self, max_price: float) -> PriceBudgetIterator:
        return PriceBudgetIterator(self._products, max_price)

    def add_product(self, product: dict):
        self._products.append(product)
