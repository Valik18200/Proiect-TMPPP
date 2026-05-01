from abc import ABC, abstractmethod


class DisplayDevice(ABC):
    @abstractmethod
    def render(self, content: str) -> str:
        pass


class PhoneDisplay(DisplayDevice):
    def render(self, content: str) -> str:
        return f"📱 [Telefon] {content} (optimizat mobil)"


class TabletDisplay(DisplayDevice):
    def render(self, content: str) -> str:
        return f"📟 [Tableta] {content} (ecran mare)"


class WebDisplay(DisplayDevice):
    def render(self, content: str) -> str:
        return f"💻 [Web] {content} (desktop full HD)"


class CatalogView(ABC):
    def __init__(self, device: DisplayDevice):
        self._device = device

    @abstractmethod
    def show(self) -> str:
        pass


class ListCatalogView(CatalogView):
    def __init__(self, device: DisplayDevice, products: list):
        super().__init__(device)
        self._products = products

    def show(self) -> str:
        content = "Lista produse iuti: " + ", ".join(self._products)
        return self._device.render(content)


class GridCatalogView(CatalogView):
    def __init__(self, device: DisplayDevice, products: list):
        super().__init__(device)
        self._products = products

    def show(self) -> str:
        content = "Grid: 🔥[" + "] 🔥[".join(self._products) + "]"
        return self._device.render(content)


class DetailCatalogView(CatalogView):
    def __init__(self, device: DisplayDevice, product_name: str, price: float, heat_level: str = ""):
        super().__init__(device)
        self._product_name = product_name
        self._price = price
        self._heat_level = heat_level

    def show(self) -> str:
        heat_info = f" - Nivel iuteala: {self._heat_level}" if self._heat_level else ""
        content = f"Detalii: {self._product_name} - {self._price:.2f} LEI{heat_info}"
        return self._device.render(content)