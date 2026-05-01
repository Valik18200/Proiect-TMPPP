# command.py
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self) -> str:
        pass

    @abstractmethod
    def undo(self) -> str:
        pass


class Inventory:
    def __init__(self):
        self._stock = {}

    def add(self, sauce: str, qty: int):
        self._stock[sauce] = self._stock.get(sauce, 0) + qty

    def remove(self, sauce: str, qty: int) -> bool:
        if self._stock.get(sauce, 0) >= qty:
            self._stock[sauce] -= qty
            return True
        return False

    def get_stock(self, sauce: str) -> int:
        return self._stock.get(sauce, 0)

    def __str__(self):
        return str(self._stock)


class AddStockCommand(Command):
    def __init__(self, inventory: Inventory, sauce: str, qty: int):
        self._inventory = inventory
        self._sauce = sauce
        self._qty = qty

    def execute(self) -> str:
        self._inventory.add(self._sauce, self._qty)
        return f"🌶️ Adaugat {self._qty}x {self._sauce} in stoc"

    def undo(self) -> str:
        self._inventory.remove(self._sauce, self._qty)
        return f"↩️ Undo: scos {self._qty}x {self._sauce} din stoc"


class RemoveStockCommand(Command):
    def __init__(self, inventory: Inventory, sauce: str, qty: int):
        self._inventory = inventory
        self._sauce = sauce
        self._qty = qty

    def execute(self) -> str:
        if self._inventory.remove(self._sauce, self._qty):
            return f"🔥 Scos {self._qty}x {self._sauce} din stoc"
        return f"❌ Eroare: stoc insuficient pentru {self._sauce}"

    def undo(self) -> str:
        self._inventory.add(self._sauce, self._qty)
        return f"↩️ Undo: readaugat {self._qty}x {self._sauce}"


class UpdatePriceCommand(Command):
    def __init__(self, prices: dict, sauce: str, new_price: float):
        self._prices = prices
        self._sauce = sauce
        self._new_price = new_price
        self._old_price = prices.get(sauce, 0)

    def execute(self) -> str:
        self._old_price = self._prices.get(self._sauce, 0)
        self._prices[self._sauce] = self._new_price
        return f"💰 Pret {self._sauce}: {self._old_price:.2f} -> {self._new_price:.2f} LEI"

    def undo(self) -> str:
        self._prices[self._sauce] = self._old_price
        return f"↩️ Undo pret {self._sauce}: {self._new_price:.2f} -> {self._old_price:.2f} LEI"


class CommandHistory:
    def __init__(self):
        self._history = []
        self._redo_stack = []

    def execute(self, command: Command) -> str:
        result = command.execute()
        self._history.append(command)
        self._redo_stack.clear()
        return result

    def undo(self) -> str:
        if not self._history:
            return "Nimic de anulat"
        cmd = self._history.pop()
        self._redo_stack.append(cmd)
        return cmd.undo()

    def redo(self) -> str:
        if not self._redo_stack:
            return "Nimic de refacut"
        cmd = self._redo_stack.pop()
        self._history.append(cmd)
        return cmd.execute()