from abc import ABC, abstractmethod


class ProductService(ABC):
    @abstractmethod
    def get_product_info(self, product_id: str) -> str:
        pass

    @abstractmethod
    def update_price(self, product_id: str, new_price: float) -> str:
        pass


class RealProductService(ProductService):
    def __init__(self):
        self._products = {
            "HP001": {"name": "Ardei iute Habanero", "price": 29.99, "heat": "Picant"},
            "HP002": {"name": "Ardei iute Carolina Reaper", "price": 49.99, "heat": "Inferno"},
            "HP003": {"name": "Sos iute Sriracha", "price": 19.99, "heat": "Mediu"},
            "SS001": {"name": "Sos iute Ghost Pepper", "price": 39.99, "heat": "Extra-Picant"},
            "PA001": {"name": "Pasta iute Harissa", "price": 24.99, "heat": "Picant"},
            "US001": {"name": "Usturoi iute fermentat", "price": 34.99, "heat": "Mediu"},
        }

    def get_product_info(self, product_id: str) -> str:
        product = self._products.get(product_id)
        if product:
            return f"{product['name']} - {product['price']:.2f} LEI (🔥 {product['heat']})"
        return "Produs negasit"

    def update_price(self, product_id: str, new_price: float) -> str:
        if product_id in self._products:
            old = self._products[product_id]["price"]
            self._products[product_id]["price"] = new_price
            return f"Pret actualizat: {old:.2f} -> {new_price:.2f} LEI"
        return "Produs negasit"


class CachingProxy(ProductService):
    def __init__(self, service: ProductService):
        self._service = service
        self._cache = {}

    def get_product_info(self, product_id: str) -> str:
        if product_id in self._cache:
            return f"[CACHE] {self._cache[product_id]}"
        result = self._service.get_product_info(product_id)
        self._cache[product_id] = result
        return f"[DB] {result}"

    def update_price(self, product_id: str, new_price: float) -> str:
        self._cache.pop(product_id, None)
        return self._service.update_price(product_id, new_price)


class AccessControlProxy(ProductService):
    def __init__(self, service: ProductService, role: str):
        self._service = service
        self._role = role

    def get_product_info(self, product_id: str) -> str:
        return self._service.get_product_info(product_id)

    def update_price(self, product_id: str, new_price: float) -> str:
        if self._role != "admin":
            return f"⛔ Acces refuzat: rolul '{self._role}' nu poate modifica preturile"
        return self._service.update_price(product_id, new_price)


class LoggingProxy(ProductService):
    def __init__(self, service: ProductService):
        self._service = service
        self.logs = []

    def get_product_info(self, product_id: str) -> str:
        self.logs.append(f"GET {product_id}")
        return self._service.get_product_info(product_id)

    def update_price(self, product_id: str, new_price: float) -> str:
        self.logs.append(f"UPDATE {product_id} -> {new_price} LEI")
        return self._service.update_price(product_id, new_price)