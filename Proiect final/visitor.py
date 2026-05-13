"""
VISITOR — Operatii aplicate pe produse fara modificarea claselor lor:
calcul taxe, generare eticheta, audit iuteala, export CSV.
"""
from abc import ABC, abstractmethod


# ─────────────────────────────────────────
'  ELEMENT interface'
# ─────────────────────────────────────────

class SpiceElement(ABC):
    @abstractmethod
    def accept(self, visitor: "SpiceVisitor"):
        pass


# ─────────────────────────────────────────
'  ELEMENTE CONCRETE (produse)'
# ─────────────────────────────────────────

class HotSauceElement(SpiceElement):
    def __init__(self, name: str, price: float, scoville: int, volume_ml: int):
        self.name      = name
        self.price     = price
        self.scoville  = scoville
        self.volume_ml = volume_ml

    def accept(self, visitor: "SpiceVisitor"):
        return visitor.visit_hot_sauce(self)


class SpiceElement2(SpiceElement):
    def __init__(self, name: str, price: float, scoville: int, weight_g: int):
        self.name     = name
        self.price    = price
        self.scoville = scoville
        self.weight_g = weight_g

    def accept(self, visitor: "SpiceVisitor"):
        return visitor.visit_spice(self)


class DriedPepperElement(SpiceElement):
    def __init__(self, name: str, price: float, scoville: int, whole: bool):
        self.name     = name
        self.price    = price
        self.scoville = scoville
        self.whole    = whole

    def accept(self, visitor: "SpiceVisitor"):
        return visitor.visit_dried_pepper(self)


class HotSaltElement(SpiceElement):
    def __init__(self, name: str, price: float, scoville: int, weight_g: int):
        self.name     = name
        self.price    = price
        self.scoville = scoville
        self.weight_g = weight_g

    def accept(self, visitor: "SpiceVisitor"):
        return visitor.visit_hot_salt(self)


# ─────────────────────────────────────────
'  VISITOR interface'
# ─────────────────────────────────────────

class SpiceVisitor(ABC):
    @abstractmethod
    def visit_hot_sauce(self, element: HotSauceElement):
        pass

    @abstractmethod
    def visit_spice(self, element: SpiceElement2):
        pass

    @abstractmethod
    def visit_dried_pepper(self, element: DriedPepperElement):
        pass

    @abstractmethod
    def visit_hot_salt(self, element: HotSaltElement):
        pass


# ─────────────────────────────────────────
'  VIZITATORI CONCRETI'
# ─────────────────────────────────────────

class TaxCalculatorVisitor(SpiceVisitor):
    """Calculeaza TVA (19%) + taxa de iuteala pentru produse > 100k SHU."""
    TAX_RATE        = 0.19
    HEAT_TAX_RATE   = 0.05   # 5% taxa suplimentara produse extreme

    def _base_tax(self, price: float, scoville: int) -> str:
        vat    = price * self.TAX_RATE
        heat   = price * self.HEAT_TAX_RATE if scoville >= 100_000 else 0
        total  = price + vat + heat
        return (f"  TVA: {vat:.2f} LEI"
                + (f" + taxa iuteala: {heat:.2f} LEI" if heat else "")
                + f" → pret final: {total:.2f} LEI")

    def visit_hot_sauce(self, e: HotSauceElement) -> str:
        return f"[TAX] {e.name}: {self._base_tax(e.price, e.scoville)}"

    def visit_spice(self, e: SpiceElement2) -> str:
        return f"[TAX] {e.name}: {self._base_tax(e.price, e.scoville)}"

    def visit_dried_pepper(self, e: DriedPepperElement) -> str:
        return f"[TAX] {e.name}: {self._base_tax(e.price, e.scoville)}"

    def visit_hot_salt(self, e: HotSaltElement) -> str:
        return f"[TAX] {e.name}: {self._base_tax(e.price, e.scoville)}"


class LabelGeneratorVisitor(SpiceVisitor):
    """Genereaza eticheta de produs pentru ambalaj."""

    def _heat_badge(self, shu: int) -> str:
        if shu < 5_000:    return "🟢 BLAND"
        if shu < 50_000:   return "🟡 MEDIU"
        if shu < 500_000:  return "🟠 IUTE"
        return "🔴 EXTREM"

    def visit_hot_sauce(self, e: HotSauceElement) -> str:
        return (f"[ETICHETA] {e.name} | {e.volume_ml}ml | "
                f"{e.scoville} SHU {self._heat_badge(e.scoville)}")

    def visit_spice(self, e: SpiceElement2) -> str:
        return (f"[ETICHETA] {e.name} | {e.weight_g}g | "
                f"{e.scoville} SHU {self._heat_badge(e.scoville)}")

    def visit_dried_pepper(self, e: DriedPepperElement) -> str:
        forma = "INTREG" if e.whole else "MACINAT"
        return (f"[ETICHETA] {e.name} | {forma} | "
                f"{e.scoville} SHU {self._heat_badge(e.scoville)}")

    def visit_hot_salt(self, e: HotSaltElement) -> str:
        return (f"[ETICHETA] {e.name} | {e.weight_g}g | "
                f"{e.scoville} SHU {self._heat_badge(e.scoville)}")


class CSVExportVisitor(SpiceVisitor):
    """Exporta datele produsului in format CSV."""

    def visit_hot_sauce(self, e: HotSauceElement) -> str:
        return f"sos_iute,{e.name},{e.price},{e.scoville},{e.volume_ml}ml"

    def visit_spice(self, e: SpiceElement2) -> str:
        return f"condiment,{e.name},{e.price},{e.scoville},{e.weight_g}g"

    def visit_dried_pepper(self, e: DriedPepperElement) -> str:
        forma = "intreg" if e.whole else "macinat"
        return f"ardei_deshidratat,{e.name},{e.price},{e.scoville},{forma}"

    def visit_hot_salt(self, e: HotSaltElement) -> str:
        return f"sare_iute,{e.name},{e.price},{e.scoville},{e.weight_g}g"
