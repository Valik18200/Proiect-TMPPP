# memento.py
import copy
from datetime import datetime


class CartMemento:
    def __init__(self, items: list, timestamp: str):
        self._items = copy.deepcopy(items)
        self._timestamp = timestamp

    @property
    def items(self) -> list:
        return copy.deepcopy(self._items)

    @property
    def timestamp(self) -> str:
        return self._timestamp


class ShoppingCart:
    def __init__(self):
        self._items = []

    def add_item(self, name: str, price: float, scoville: int = 0):
        self._items.append({"name": name, "price": price, "scoville": scoville})

    def remove_last(self):
        if self._items:
            self._items.pop()

    def get_total(self) -> float:
        return sum(item["price"] for item in self._items)

    def get_total_scoville(self) -> int:
        return sum(item.get("scoville", 0) for item in self._items)

    def save(self) -> CartMemento:
        return CartMemento(self._items, datetime.now().strftime("%H:%M:%S"))

    def restore(self, memento: CartMemento):
        self._items = memento.items

    def __str__(self):
        if not self._items:
            return "  🛒 Cosul este gol"
        lines = []
        for item in self._items:
            scoville_info = f" ({item.get('scoville', 0):,} SHU)" if item.get('scoville', 0) > 0 else ""
            lines.append(f"    - {item['name']}{scoville_info}: {item['price']:.2f} LEI")
        lines.append(f"    🔥 Total iuteala: {self.get_total_scoville():,} SHU")
        lines.append(f"    💰 Total plata: {self.get_total():.2f} LEI")
        return "\n".join(lines)


class CartHistory:
    def __init__(self):
        self._snapshots: list[CartMemento] = []

    def save(self, memento: CartMemento):
        self._snapshots.append(memento)

    def get_snapshot(self, index: int) -> CartMemento:
        return self._snapshots[index]

    def list_snapshots(self) -> list[str]:
        return [f"[{i}] {s.timestamp} - {len(s.items)} produse" for i, s in enumerate(self._snapshots)]