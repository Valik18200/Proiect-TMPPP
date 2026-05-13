"""
MEDIATOR — Coordoneaza comunicarea intre subsistemele magazinului
(inventar, pret, notificari, analitice) fara cuplare directa intre ele.
"""
from abc import ABC, abstractmethod
from typing import List


class StoreMediator(ABC):
    @abstractmethod
    def notify(self, sender: str, event: str, data: dict):
        pass


# ─────────────────────────────────────────
'  COMPONENTE (Colleagues)'
# ─────────────────────────────────────────

class InventoryComponent:
    def __init__(self, mediator: StoreMediator):
        self._mediator = mediator
        self._stock = {
            "Sriracha Original":     30,
            "Ghost Pepper Inferno":  10,
            "Cayenne Pudra":         40,
            "Carolina Reaper Pudra":  8,
        }

    def sell(self, product: str, qty: int):
        if self._stock.get(product, 0) >= qty:
            self._stock[product] -= qty
            self._mediator.notify("Inventory", "SOLD", {
                "product": product, "qty": qty,
                "remaining": self._stock[product]
            })
        else:
            self._mediator.notify("Inventory", "OUT_OF_STOCK", {"product": product})

    def restock(self, product: str, qty: int):
        self._stock[product] = self._stock.get(product, 0) + qty
        self._mediator.notify("Inventory", "RESTOCKED", {
            "product": product, "qty": qty,
            "total": self._stock[product]
        })

    def get_stock(self, product: str) -> int:
        return self._stock.get(product, 0)


class PricingComponent:
    def __init__(self, mediator: StoreMediator):
        self._mediator = mediator
        self._prices = {
            "Sriracha Original":     39.99,
            "Ghost Pepper Inferno":  69.99,
            "Cayenne Pudra":         24.99,
            "Carolina Reaper Pudra": 79.99,
        }

    def update_price(self, product: str, new_price: float):
        old = self._prices.get(product, 0)
        self._prices[product] = new_price
        self._mediator.notify("Pricing", "PRICE_UPDATED", {
            "product": product, "old": old, "new": new_price
        })

    def get_price(self, product: str) -> float:
        return self._prices.get(product, 0.0)


class NotificationComponent:
    def __init__(self, mediator: StoreMediator):
        self._mediator = mediator
        self.sent: List[str] = []

    def send(self, message: str):
        self.sent.append(message)

    def receive_event(self, event: str, data: dict):
        if event == "OUT_OF_STOCK":
            self.send(f"📧 STOC EPUIZAT: {data['product']}")
        elif event == "RESTOCKED":
            self.send(f"📧 REAPROVIZIONAT: {data['product']} (+{data['qty']})")
        elif event == "PRICE_UPDATED":
            self.send(f"📧 PRET MODIFICAT: {data['product']} "
                      f"{data['old']:.2f}→{data['new']:.2f} LEI")


class AnalyticsComponent:
    def __init__(self, mediator: StoreMediator):
        self._mediator = mediator
        self.events: List[dict] = []

    def record(self, event: str, data: dict):
        self.events.append({"event": event, **data})

    def summary(self) -> str:
        sales = [e for e in self.events if e["event"] == "SOLD"]
        total_items = sum(e.get("qty", 0) for e in sales)
        return f"Analitice: {len(sales)} vanzari, {total_items} produse vandute"


# ─────────────────────────────────────────
'  MEDIATOR CONCRET'
# ─────────────────────────────────────────

class SpiceStoreMediator(StoreMediator):
    def __init__(self):
        self.inventory    : InventoryComponent    = None
        self.pricing      : PricingComponent      = None
        self.notification : NotificationComponent = None
        self.analytics    : AnalyticsComponent    = None

    def setup(self):
        self.inventory    = InventoryComponent(self)
        self.pricing      = PricingComponent(self)
        self.notification = NotificationComponent(self)
        self.analytics    = AnalyticsComponent(self)

    def notify(self, sender: str, event: str, data: dict):
        if self.analytics:
            self.analytics.record(event, data)
        if self.notification:
            self.notification.receive_event(event, data)
