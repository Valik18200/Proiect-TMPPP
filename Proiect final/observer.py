"""
OBSERVER — Notificari automate la schimbari de stoc, pret sau produse noi.
"""
from abc import ABC, abstractmethod
from typing import List


# ─────────────────────────────────────────
#  OBSERVER interface
# ─────────────────────────────────────────

class SpiceObserver(ABC):
    @abstractmethod
    def update(self, event: str, data: dict):
        pass


# ─────────────────────────────────────────
'  OBSERVATORI CONCRETI'
# ─────────────────────────────────────────

class EmailSubscriber(SpiceObserver):
    def __init__(self, email: str):
        self.email = email
        self.received: List[str] = []

    def update(self, event: str, data: dict):
        msg = f"[EMAIL → {self.email}] {event}: {data}"
        self.received.append(msg)

    def __str__(self):
        return f"EmailSubscriber({self.email})"


class StockAlertObserver(SpiceObserver):
    """Se activeaza cand stocul scade sub un prag."""
    def __init__(self, threshold: int = 5):
        self.threshold = threshold
        self.alerts: List[str] = []

    def update(self, event: str, data: dict):
        if event == "STOCK_LOW" and data.get("stock", 99) < self.threshold:
            msg = (f"[ALERT STOC] {data['product']} are doar "
                   f"{data['stock']} buc ramase!")
            self.alerts.append(msg)

    def __str__(self):
        return f"StockAlertObserver(prag={self.threshold})"


class PriceWatchObserver(SpiceObserver):
    """Urmareste modificarile de pret."""
    def __init__(self, name: str):
        self.name = name
        self.price_changes: List[str] = []

    def update(self, event: str, data: dict):
        if event == "PRICE_CHANGED":
            msg = (f"[PRICE WATCH - {self.name}] {data['product']}: "
                   f"{data['old_price']:.2f} → {data['new_price']:.2f} LEI")
            self.price_changes.append(msg)

    def __str__(self):
        return f"PriceWatchObserver({self.name})"


class AuditLogObserver(SpiceObserver):
    """Inregistreaza toate evenimentele pentru audit."""
    def __init__(self):
        self.log: List[str] = []

    def update(self, event: str, data: dict):
        self.log.append(f"[AUDIT] {event} | {data}")

    def __str__(self):
        return "AuditLogObserver"


# ─────────────────────────────────────────
'  SUBJECT'
# ─────────────────────────────────────────

class SpiceInventorySubject:
    def __init__(self):
        self._observers: List[SpiceObserver] = []
        self._stock = {
            "Sriracha Original":        30,
            "Ghost Pepper Inferno":     10,
            "Cayenne Pudra":            40,
            "Jalapeno Intreg":          25,
            "Carolina Reaper Pudra":     8,
        }
        self._prices = {
            "Sriracha Original":        39.99,
            "Ghost Pepper Inferno":     69.99,
            "Cayenne Pudra":            24.99,
            "Jalapeno Intreg":          27.99,
            "Carolina Reaper Pudra":    79.99,
        }

    def subscribe(self, observer: SpiceObserver):
        self._observers.append(observer)

    def unsubscribe(self, observer: SpiceObserver):
        self._observers.remove(observer)

    def notify(self, event: str, data: dict):
        for obs in self._observers:
            obs.update(event, data)

    def sell(self, product: str, qty: int = 1):
        if product in self._stock:
            self._stock[product] = max(0, self._stock[product] - qty)
            stock_left = self._stock[product]
            self.notify("SALE", {"product": product, "qty": qty, "stock": stock_left})
            if stock_left < 5:
                self.notify("STOCK_LOW", {"product": product, "stock": stock_left})

    def update_price(self, product: str, new_price: float):
        if product in self._prices:
            old = self._prices[product]
            self._prices[product] = new_price
            self.notify("PRICE_CHANGED", {
                "product": product, "old_price": old, "new_price": new_price
            })

    def add_product(self, product: str, price: float, stock: int):
        self._stock[product]  = stock
        self._prices[product] = price
        self.notify("NEW_PRODUCT", {"product": product, "price": price, "stock": stock})

    def get_stock(self, product: str) -> int:
        return self._stock.get(product, 0)
