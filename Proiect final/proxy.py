from abc import ABC, abstractmethod


class SpiceService(ABC):
    @abstractmethod
    def get_product_info(self, product_id: str) -> str:
        pass

    @abstractmethod
    def update_price(self, product_id: str, new_price: float) -> str:
        pass


class RealSpiceService(SpiceService):
    def __init__(self):
        self._products = {
            "HS001": {"name": "Sriracha Original",       "price": 39.99,  "scoville": 2_200},
            "HS002": {"name": "Ghost Pepper Inferno",    "price": 69.99,  "scoville": 100_000},
            "HS003": {"name": "Habanero Mango Blast",    "price": 54.99,  "scoville": 8_000},
            "SP001": {"name": "Cayenne Pudra",           "price": 24.99,  "scoville": 40_000},
            "SP002": {"name": "Amestec Cajun",           "price": 29.99,  "scoville": 5_000},
            "DP001": {"name": "Jalapeno Intreg",         "price": 27.99,  "scoville": 8_000},
            "DP002": {"name": "Carolina Reaper Pudra",   "price": 79.99,  "scoville": 2_200_000},
            "SL001": {"name": "Sare Roz cu Chili",       "price": 18.99,  "scoville": 5_000},
        }

    def get_product_info(self, product_id: str) -> str:
        p = self._products.get(product_id)
        if p:
            return f"{p['name']} - {p['price']:.2f} LEI | {p['scoville']} SHU"
        return "Produs negasit"

    def update_price(self, product_id: str, new_price: float) -> str:
        if product_id in self._products:
            old = self._products[product_id]["price"]
            self._products[product_id]["price"] = new_price
            return f"Pret actualizat: {old:.2f} -> {new_price:.2f} LEI"
        return "Produs negasit"


class CachingProxy(SpiceService):
    """Proxy de caching — evita interogari repetate catre serviciu."""
    def __init__(self, service: SpiceService):
        self._service = service
        self._cache   = {}

    def get_product_info(self, product_id: str) -> str:
        if product_id in self._cache:
            return f"[CACHE] {self._cache[product_id]}"
        result = self._service.get_product_info(product_id)
        self._cache[product_id] = result
        return f"[DB] {result}"

    def update_price(self, product_id: str, new_price: float) -> str:
        self._cache.pop(product_id, None)   # invalideaza cache
        return self._service.update_price(product_id, new_price)


class AccessControlProxy(SpiceService):
    """Proxy de control acces — doar admin poate modifica preturile."""
    def __init__(self, service: SpiceService, role: str):
        self._service = service
        self._role    = role

    def get_product_info(self, product_id: str) -> str:
        return self._service.get_product_info(product_id)

    def update_price(self, product_id: str, new_price: float) -> str:
        if self._role != "admin":
            return f"Acces refuzat: rolul '{self._role}' nu poate modifica preturile"
        return self._service.update_price(product_id, new_price)


class LoggingProxy(SpiceService):
    """Proxy de logging — inregistreaza toate operatiunile efectuate."""
    def __init__(self, service: SpiceService):
        self._service = service
        self.logs     = []

    def get_product_info(self, product_id: str) -> str:
        self.logs.append(f"GET {product_id}")
        return self._service.get_product_info(product_id)

    def update_price(self, product_id: str, new_price: float) -> str:
        self.logs.append(f"UPDATE {product_id} -> {new_price:.2f} LEI")
        return self._service.update_price(product_id, new_price)
