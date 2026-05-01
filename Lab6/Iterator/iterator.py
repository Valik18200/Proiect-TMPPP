# iterator.py
class HotSauce:
    def __init__(self, name: str, price: float, category: str, scoville: int):
        self.name = name
        self.price = price
        self.category = category
        self.scoville = scoville

    def __str__(self):
        scoville_str = f"{self.scoville:,} SHU" if self.scoville > 0 else "mild"
        return f"🌶️ {self.name} ({self.category}) - {self.price:.2f} LEI | {scoville_str}"


class SauceCollection:
    def __init__(self):
        self._sauces = []

    def add(self, sauce: HotSauce):
        self._sauces.append(sauce)

    def __len__(self):
        return len(self._sauces)

    def iterator(self):
        return SauceIterator(self._sauces)

    def price_range_iterator(self, min_price: float, max_price: float):
        filtered = [s for s in self._sauces if min_price <= s.price <= max_price]
        return SauceIterator(filtered)

    def category_iterator(self, category: str):
        filtered = [s for s in self._sauces if s.category.lower() == category.lower()]
        return SauceIterator(filtered)

    def scoville_range_iterator(self, min_scoville: int, max_scoville: int):
        filtered = [s for s in self._sauces if min_scoville <= s.scoville <= max_scoville]
        return SauceIterator(filtered)

    def extreme_iterator(self, min_scoville: int = 100000):
        filtered = [s for s in self._sauces if s.scoville >= min_scoville]
        return SauceIterator(filtered)


class SauceIterator:
    def __init__(self, sauces: list):
        self._sauces = sauces
        self._index = 0

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self) -> HotSauce:
        if self._index >= len(self._sauces):
            raise StopIteration
        sauce = self._sauces[self._index]
        self._index += 1
        return sauce

    def has_next(self) -> bool:
        return self._index < len(self._sauces)

    def reset(self):
        self._index = 0