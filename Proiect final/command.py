"""
COMMAND — Operatii pe cosul de cumparaturi ca obiecte,
cu suport pentru undo/redo.
"""
from abc import ABC, abstractmethod
from typing import List


# ─────────────────────────────────────────
'  RECEIVER'
# ─────────────────────────────────────────

class ShoppingCart:
    def __init__(self):
        self._items: dict = {}   # {product: qty}
        self._prices: dict = {
            "Sriracha Original":        39.99,
            "Ghost Pepper Inferno":     69.99,
            "Cayenne Pudra":            24.99,
            "Jalapeno Intreg":          27.99,
            "Sare Roz cu Chili":        18.99,
            "Habanero Mango Blast":     54.99,
            "Carolina Reaper Pudra":    79.99,
            "Amestec Cajun":            29.99,
        }

    def add(self, product: str, qty: int = 1):
        self._items[product] = self._items.get(product, 0) + qty

    def remove(self, product: str, qty: int = 1):
        if product in self._items:
            self._items[product] -= qty
            if self._items[product] <= 0:
                del self._items[product]

    def apply_discount(self, product: str, pct: float):
        if product in self._prices:
            self._prices[product] *= (1 - pct)

    def remove_discount(self, product: str, pct: float):
        if product in self._prices:
            self._prices[product] /= (1 - pct)

    def get_total(self) -> float:
        return sum(
            self._prices.get(p, 0) * qty
            for p, qty in self._items.items()
        )

    def get_items(self) -> dict:
        return dict(self._items)

    def display(self) -> str:
        if not self._items:
            return "Cosul este gol."
        lines = ["=== COS DE CUMPARATURI ==="]
        for product, qty in self._items.items():
            price = self._prices.get(product, 0)
            lines.append(f"  {product:<30} x{qty}  {price * qty:>8.2f} LEI")
        lines.append(f"  {'TOTAL':<30}      {self.get_total():>8.2f} LEI")
        return "\n".join(lines)


# ─────────────────────────────────────────
'  COMMAND interface'
# ─────────────────────────────────────────

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

    @abstractmethod
    def description(self) -> str:
        pass


# ─────────────────────────────────────────
'  COMENZI CONCRETE'
# ─────────────────────────────────────────

class AddToCartCommand(Command):
    def __init__(self, cart: ShoppingCart, product: str, qty: int = 1):
        self._cart    = cart
        self._product = product
        self._qty     = qty

    def execute(self):
        self._cart.add(self._product, self._qty)

    def undo(self):
        self._cart.remove(self._product, self._qty)

    def description(self) -> str:
        return f"Adauga {self._product} x{self._qty}"


class RemoveFromCartCommand(Command):
    def __init__(self, cart: ShoppingCart, product: str, qty: int = 1):
        self._cart    = cart
        self._product = product
        self._qty     = qty

    def execute(self):
        self._cart.remove(self._product, self._qty)

    def undo(self):
        self._cart.add(self._product, self._qty)

    def description(self) -> str:
        return f"Elimina {self._product} x{self._qty}"


class ApplyDiscountCommand(Command):
    def __init__(self, cart: ShoppingCart, product: str, discount_pct: float):
        self._cart     = cart
        self._product  = product
        self._discount = discount_pct

    def execute(self):
        self._cart.apply_discount(self._product, self._discount)

    def undo(self):
        self._cart.remove_discount(self._product, self._discount)

    def description(self) -> str:
        return f"Aplica reducere {self._discount*100:.0f}% la {self._product}"


class ClearCartCommand(Command):
    def __init__(self, cart: ShoppingCart):
        self._cart    = cart
        self._backup  = {}

    def execute(self):
        self._backup = dict(cart._items for cart in [self._cart])[0] \
            if False else dict(self._cart._items)
        self._cart._items.clear()

    def undo(self):
        self._cart._items = dict(self._backup)

    def description(self) -> str:
        return "Goleste cosul"


# ─────────────────────────────────────────
'  INVOKER cu undo/redo'
# ─────────────────────────────────────────

class CartCommandInvoker:
    def __init__(self):
        self._history: List[Command] = []
        self._redo_stack: List[Command] = []

    def execute(self, command: Command):
        command.execute()
        self._history.append(command)
        self._redo_stack.clear()

    def undo(self) -> str:
        if not self._history:
            return "Nimic de anulat."
        cmd = self._history.pop()
        cmd.undo()
        self._redo_stack.append(cmd)
        return f"Anulat: {cmd.description()}"

    def redo(self) -> str:
        if not self._redo_stack:
            return "Nimic de refacut."
        cmd = self._redo_stack.pop()
        cmd.execute()
        self._history.append(cmd)
        return f"Refacut: {cmd.description()}"

    def history(self) -> List[str]:
        return [c.description() for c in self._history]
