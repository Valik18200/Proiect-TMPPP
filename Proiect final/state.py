"""
STATE — Ciclul de viata al unei comenzi:
Nou → Confirmat → In Pregatire → Expediat → Livrat / Anulat
"""
from abc import ABC, abstractmethod


class Order:
    """Context — comanda care isi schimba comportamentul in functie de stare."""
    def __init__(self, order_id: str, product: str, total: float):
        self.order_id = order_id
        self.product  = product
        self.total    = total
        self._state: "OrderState" = NewOrderState(self)

    def set_state(self, state: "OrderState"):
        self._state = state

    def get_state_name(self) -> str:
        return self._state.name()

    def confirm(self) -> str:
        return self._state.confirm()

    def prepare(self) -> str:
        return self._state.prepare()

    def ship(self) -> str:
        return self._state.ship()

    def deliver(self) -> str:
        return self._state.deliver()

    def cancel(self) -> str:
        return self._state.cancel()

    def __str__(self):
        return (f"Comanda {self.order_id} | {self.product} | "
                f"{self.total:.2f} LEI | Stare: {self.get_state_name()}")


class OrderState(ABC):
    def __init__(self, order: Order):
        self._order = order

    @abstractmethod
    def name(self) -> str:
        pass

    def confirm(self) -> str:
        return f"❌ Actiunea 'confirma' nu e permisa in starea '{self.name()}'"

    def prepare(self) -> str:
        return f"❌ Actiunea 'pregateste' nu e permisa in starea '{self.name()}'"

    def ship(self) -> str:
        return f"❌ Actiunea 'expediaza' nu e permisa in starea '{self.name()}'"

    def deliver(self) -> str:
        return f"❌ Actiunea 'livreaza' nu e permisa in starea '{self.name()}'"

    def cancel(self) -> str:
        return f"❌ Actiunea 'anuleaza' nu e permisa in starea '{self.name()}'"


class NewOrderState(OrderState):
    def name(self) -> str:
        return "NOU"

    def confirm(self) -> str:
        self._order.set_state(ConfirmedOrderState(self._order))
        return f"✅ Comanda {self._order.order_id} confirmata."

    def cancel(self) -> str:
        self._order.set_state(CancelledOrderState(self._order))
        return f"🚫 Comanda {self._order.order_id} anulata (era noua)."


class ConfirmedOrderState(OrderState):
    def name(self) -> str:
        return "CONFIRMAT"

    def prepare(self) -> str:
        self._order.set_state(PreparingOrderState(self._order))
        return f"📦 Comanda {self._order.order_id} in pregatire."

    def cancel(self) -> str:
        self._order.set_state(CancelledOrderState(self._order))
        return f"🚫 Comanda {self._order.order_id} anulata (era confirmata)."


class PreparingOrderState(OrderState):
    def name(self) -> str:
        return "IN PREGATIRE"

    def ship(self) -> str:
        self._order.set_state(ShippedOrderState(self._order))
        return f"🚚 Comanda {self._order.order_id} expediata."

    def cancel(self) -> str:
        self._order.set_state(CancelledOrderState(self._order))
        return f"🚫 Comanda {self._order.order_id} anulata (era in pregatire)."


class ShippedOrderState(OrderState):
    def name(self) -> str:
        return "EXPEDIAT"

    def deliver(self) -> str:
        self._order.set_state(DeliveredOrderState(self._order))
        return f"✅ Comanda {self._order.order_id} livrata cu succes!"


class DeliveredOrderState(OrderState):
    def name(self) -> str:
        return "LIVRAT"


class CancelledOrderState(OrderState):
    def name(self) -> str:
        return "ANULAT"
