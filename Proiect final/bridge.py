from abc import ABC, abstractmethod


# ─────────────────────────────────────────
#  IMPLEMENTARE — dispozitive de afisare
# ─────────────────────────────────────────

class DisplayDevice(ABC):
    @abstractmethod
    def render(self, content: str) -> str:
        pass


class PhoneDisplay(DisplayDevice):
    def render(self, content: str) -> str:
        return f"[Telefon] {content} (320x480)"


class TabletDisplay(DisplayDevice):
    def render(self, content: str) -> str:
        return f"[Tableta] {content} (768x1024)"


class WebDisplay(DisplayDevice):
    def render(self, content: str) -> str:
        return f"[Web] {content} (1920x1080)"


# ─────────────────────────────────────────
'  ABSTRACTIE — tipuri de vizualizare catalog'
# ─────────────────────────────────────────

class SpiceCatalogView(ABC):
    def __init__(self, device: DisplayDevice):
        self._device = device

    @abstractmethod
    def show(self) -> str:
        pass


class ListCatalogView(SpiceCatalogView):
    """Afiseaza produsele ca lista simpla cu SHU."""
    def __init__(self, device: DisplayDevice, products: list):
        super().__init__(device)
        self._products = products

    def show(self) -> str:
        content = "Lista: " + ", ".join(self._products)
        return self._device.render(content)


class GridCatalogView(SpiceCatalogView):
    """Afiseaza produsele ca grila de carduri."""
    def __init__(self, device: DisplayDevice, products: list):
        super().__init__(device)
        self._products = products

    def show(self) -> str:
        content = "Grid: [" + "] [".join(self._products) + "]"
        return self._device.render(content)


class HeatScaleCatalogView(SpiceCatalogView):
    """
    Vizualizare specifica domeniului — afiseaza produsele
    sortate dupa nivelul de iuteala (Scoville).
    """
    def __init__(self, device: DisplayDevice, products_shu: list):
        super().__init__(device)
        # products_shu = lista de tuple (nume, shu)
        self._products_shu = sorted(products_shu, key=lambda x: x[1])

    def show(self) -> str:
        items = " < ".join(f"{name}({shu}SHU)"
                           for name, shu in self._products_shu)
        content = f"Scara Scoville: {items}"
        return self._device.render(content)


class DetailCatalogView(SpiceCatalogView):
    """Afiseaza detaliile complete ale unui singur produs."""
    def __init__(self, device: DisplayDevice, product_name: str,
                 price: float, scoville: int):
        super().__init__(device)
        self._product_name = product_name
        self._price        = price
        self._scoville     = scoville

    def show(self) -> str:
        content = (f"Detalii: {self._product_name} - "
                   f"{self._price:.2f} LEI | {self._scoville} SHU")
        return self._device.render(content)
