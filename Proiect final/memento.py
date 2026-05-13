"""
MEMENTO — Salvare si restaurare a configuratiei unui profil de comanda
(produse selectate, discounturi, preferinte).
"""
from typing import List
import copy


# ─────────────────────────────────────────
'  MEMENTO'
# ─────────────────────────────────────────

class OrderSnapshot:
    """Memento — stocheaza starea unui profil de comanda."""
    def __init__(self, items: dict, discount: float, note: str):
        self._items    = copy.deepcopy(items)
        self._discount = discount
        self._note     = note

    @property
    def items(self) -> dict:
        return copy.deepcopy(self._items)

    @property
    def discount(self) -> float:
        return self._discount

    @property
    def note(self) -> str:
        return self._note

    def __str__(self):
        return (f"Snapshot[{self._note}]: "
                f"{list(self._items.keys())} discount={self._discount*100:.0f}%")


# ─────────────────────────────────────────
'  ORIGINATOR'
# ─────────────────────────────────────────

class OrderProfile:
    """Originator — configuratia unei comenzi care poate fi salvata/restaurata."""
    def __init__(self):
        self._items: dict    = {}   # {product: qty}
        self._discount: float = 0.0
        self._note: str       = ""

    def add_item(self, product: str, qty: int):
        self._items[product] = self._items.get(product, 0) + qty

    def remove_item(self, product: str):
        self._items.pop(product, None)

    def set_discount(self, discount: float):
        self._discount = discount

    def set_note(self, note: str):
        self._note = note

    def save(self) -> OrderSnapshot:
        return OrderSnapshot(self._items, self._discount, self._note)

    def restore(self, snapshot: OrderSnapshot):
        self._items    = snapshot.items
        self._discount = snapshot.discount
        self._note     = snapshot.note

    def display(self) -> str:
        if not self._items:
            return f"Profil gol | discount: {self._discount*100:.0f}%"
        items_str = ", ".join(f"{p} x{q}" for p, q in self._items.items())
        return (f"Profil: [{items_str}] | "
                f"discount: {self._discount*100:.0f}% | nota: '{self._note}'")


# ─────────────────────────────────────────
'  CARETAKER'
# ─────────────────────────────────────────

class OrderHistory:
    """Caretaker — gestioneaza istoricul snapshot-urilor."""
    def __init__(self):
        self._snapshots: List[OrderSnapshot] = []

    def save(self, profile: OrderProfile, label: str = ""):
        snapshot = profile.save()
        if label:
            snapshot._note = label
        self._snapshots.append(snapshot)

    def restore(self, profile: OrderProfile, index: int = -1):
        if not self._snapshots:
            return "Nu exista snapshot-uri salvate."
        snap = self._snapshots[index]
        profile.restore(snap)
        return f"Restaurat: {snap}"

    def list_snapshots(self) -> List[str]:
        return [str(s) for s in self._snapshots]

    def count(self) -> int:
        return len(self._snapshots)
