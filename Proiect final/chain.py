"""
CHAIN OF RESPONSIBILITY — Validarea unei comenzi trece printr-un
lant de handlere: stoc → varsta → buget → iuteala → aprobare finala.
"""
from abc import ABC, abstractmethod
from typing import Optional


class OrderRequest:
    def __init__(self, product: str, quantity: int, customer_age: int,
                 budget: float, scoville: int, price: float):
        self.product      = product
        self.quantity     = quantity
        self.customer_age = customer_age
        self.budget       = budget
        self.scoville     = scoville
        self.price        = price
        self.total        = price * quantity
        self.approved     = False
        self.notes: list  = []


class OrderHandler(ABC):
    def __init__(self):
        self._next: Optional["OrderHandler"] = None

    def set_next(self, handler: "OrderHandler") -> "OrderHandler":
        self._next = handler
        return handler

    @abstractmethod
    def handle(self, request: OrderRequest) -> str:
        pass

    def _pass_to_next(self, request: OrderRequest) -> str:
        if self._next:
            return self._next.handle(request)
        request.approved = True
        return f"✅ Comanda APROBATA: {request.product} x{request.quantity} = {request.total:.2f} LEI"


class StockCheckHandler(OrderHandler):
    def __init__(self, stock: dict):
        super().__init__()
        self._stock = stock

    def handle(self, request: OrderRequest) -> str:
        available = self._stock.get(request.product, 0)
        if available < request.quantity:
            return (f"❌ STOC INSUFICIENT: {request.product} "
                    f"(cerut: {request.quantity}, disponibil: {available})")
        request.notes.append(f"Stoc OK ({available} disponibil)")
        return self._pass_to_next(request)


class AgeVerificationHandler(OrderHandler):
    """Produsele cu > 500.000 SHU sunt doar pentru adulti."""
    ADULT_SHU_THRESHOLD = 500_000

    def handle(self, request: OrderRequest) -> str:
        if request.scoville > self.ADULT_SHU_THRESHOLD and request.customer_age < 18:
            return (f"❌ RESTRICTIE VARSTA: {request.product} ({request.scoville} SHU) "
                    f"necesita varsta minima 18 ani.")
        request.notes.append(f"Varsta OK ({request.customer_age} ani)")
        return self._pass_to_next(request)


class BudgetCheckHandler(OrderHandler):
    def handle(self, request: OrderRequest) -> str:
        if request.total > request.budget:
            return (f"❌ BUGET DEPASIT: total {request.total:.2f} LEI "
                    f"> buget {request.budget:.2f} LEI")
        request.notes.append(f"Buget OK (total {request.total:.2f} LEI)")
        return self._pass_to_next(request)


class HeatWarningHandler(OrderHandler):
    """La produse > 100.000 SHU adauga avertisment, dar nu blocheaza."""
    def handle(self, request: OrderRequest) -> str:
        if request.scoville >= 100_000:
            request.notes.append(
                f"⚠️  ATENTIE: iuteala extrema {request.scoville} SHU — "
                f"manipulati cu grija!"
            )
        return self._pass_to_next(request)


class FraudCheckHandler(OrderHandler):
    """Comenzile de peste 500 LEI necesita verificare suplimentara."""
    FRAUD_THRESHOLD = 500.0

    def handle(self, request: OrderRequest) -> str:
        if request.total > self.FRAUD_THRESHOLD:
            request.notes.append(
                f"🔍 Verificare anti-frauda efectuata (total {request.total:.2f} LEI > "
                f"{self.FRAUD_THRESHOLD:.0f} LEI)"
            )
        return self._pass_to_next(request)


def build_validation_chain(stock: dict) -> OrderHandler:
    """Construieste lantul standard de validare."""
    stock_check  = StockCheckHandler(stock)
    age_check    = AgeVerificationHandler()
    budget_check = BudgetCheckHandler()
    heat_warning = HeatWarningHandler()
    fraud_check  = FraudCheckHandler()

    stock_check.set_next(age_check).set_next(budget_check)\
               .set_next(heat_warning).set_next(fraud_check)

    return stock_check
