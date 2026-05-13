from abc import ABC, abstractmethod
from typing import List


class CatalogComponent(ABC):
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def get_price(self) -> float:
        pass

    @abstractmethod
    def display(self, indent: int = 0) -> str:
        pass


class SpiceItem(CatalogComponent):
    """Frunza — un produs individual din catalog."""

    def __init__(self, name: str, price: float, scoville: int = 0):
        super().__init__(name)
        self._price = price
        self._scoville = scoville

    @property
    def scoville(self) -> int:
        return self._scoville

    def get_price(self) -> float:
        return self._price

    def display(self, indent: int = 0) -> str:
        prefix = "  " * indent
        shu = f" | {self._scoville} SHU" if self._scoville > 0 else ""
        return f"{prefix}- {self._name}: {self._price:.2f} LEI{shu}"


class SpiceCategory(CatalogComponent):
    """Nod compus — o categorie care poate contine produse sau subcategorii."""

    def __init__(self, name: str):
        super().__init__(name)
        self._children: List[CatalogComponent] = []

    def add(self, component: CatalogComponent):
        self._children.append(component)

    def remove(self, component: CatalogComponent):
        self._children.remove(component)

    def get_children(self) -> List[CatalogComponent]:
        return list(self._children)

    def get_price(self) -> float:
        return sum(child.get_price() for child in self._children)

    def display(self, indent: int = 0) -> str:
        prefix = "  " * indent
        lines = [f"{prefix}[{self._name}] (total: {self.get_price():.2f} LEI)"]
        for child in self._children:
            lines.append(child.display(indent + 1))
        return "\n".join(lines)
