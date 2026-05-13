"""
TEMPLATE METHOD — Schelet fix pentru procesarea unui raport de magazin;
subclasele personalizeaza pasii specifici.
"""
from abc import ABC, abstractmethod
from typing import List


class SpiceReportTemplate(ABC):
    """
    Clasa de baza cu scheletul algoritmului de generare raport.
    Ordinea pasilor este fixata; subclasele redefinesc pasii abstracti.
    """

    def generate(self) -> str:
        """Metoda template — nu se suprascrie."""
        parts = []
        parts.append(self._header())
        parts.append(self._collect_data())
        parts.append(self._format_body())
        parts.append(self._add_summary())
        parts.append(self._footer())
        return "\n".join(filter(None, parts))

    # ── Pasi abstracti (obligatoriu de implementat) ──

    @abstractmethod
    def _header(self) -> str:
        pass

    @abstractmethod
    def _collect_data(self) -> str:
        pass

    @abstractmethod
    def _format_body(self) -> str:
        pass

    # ── Pasi cu implementare implicita (hook-uri) ──

    def _add_summary(self) -> str:
        return ""   # implicit fara sumar

    def _footer(self) -> str:
        return "=" * 50


# ─────────────────────────────────────────
'  RAPOARTE CONCRETE'
# ─────────────────────────────────────────

class SalesReport(SpiceReportTemplate):
    def __init__(self, sales: List[dict]):
        self._sales = sales   # [{"product": ..., "qty": ..., "total": ...}]

    def _header(self) -> str:
        return "=" * 50 + "\n   RAPORT VANZARI — ARDEI ROSU\n" + "=" * 50

    def _collect_data(self) -> str:
        return f"  Perioada: ultima luna | Tranzactii: {len(self._sales)}"

    def _format_body(self) -> str:
        if not self._sales:
            return "  Nicio vanzare inregistrata."
        lines = [f"  {'Produs':<28} {'Cant':>5} {'Total':>10}"]
        lines.append("  " + "-" * 46)
        for s in self._sales:
            lines.append(f"  {s['product']:<28} {s['qty']:>5} {s['total']:>9.2f} LEI")
        return "\n".join(lines)

    def _add_summary(self) -> str:
        total = sum(s["total"] for s in self._sales)
        return f"\n  TOTAL VANZARI: {total:.2f} LEI"


class StockReport(SpiceReportTemplate):
    def __init__(self, stock: dict):
        self._stock = stock   # {product: qty}

    def _header(self) -> str:
        return "=" * 50 + "\n   RAPORT STOC — ARDEI ROSU\n" + "=" * 50

    def _collect_data(self) -> str:
        return f"  Produse in catalog: {len(self._stock)}"

    def _format_body(self) -> str:
        lines = [f"  {'Produs':<30} {'Stoc':>6}"]
        lines.append("  " + "-" * 38)
        for product, qty in sorted(self._stock.items()):
            status = " ⚠️ " if qty < 5 else "   "
            lines.append(f"  {product:<30} {qty:>5}{status}")
        return "\n".join(lines)

    def _add_summary(self) -> str:
        low = [p for p, q in self._stock.items() if q < 5]
        if low:
            return f"\n  STOC SCAZUT: {', '.join(low)}"
        return "\n  Toate produsele au stoc suficient."


class HeatProfileReport(SpiceReportTemplate):
    """Raport specific domeniului — profilul iutelii catalogului."""
    def __init__(self, products: List[dict]):
        self._products = products

    def _header(self) -> str:
        return "=" * 50 + "\n   PROFIL IUTEALA — ARDEI ROSU\n" + "=" * 50

    def _collect_data(self) -> str:
        return f"  Produse analizate: {len(self._products)}"

    def _format_body(self) -> str:
        sorted_p = sorted(self._products, key=lambda x: x.get("scoville", 0))
        lines = [f"  {'Produs':<28} {'SHU':>10} {'Nivel':<10}"]
        lines.append("  " + "-" * 50)
        for p in sorted_p:
            shu = p.get("scoville", 0)
            if shu < 5_000:
                level = "🟢 Bland"
            elif shu < 50_000:
                level = "🟡 Mediu"
            elif shu < 500_000:
                level = "🟠 Iute"
            else:
                level = "🔴 Extrem"
            lines.append(f"  {p['name']:<28} {shu:>10,} {level}")
        return "\n".join(lines)

    def _add_summary(self) -> str:
        if not self._products:
            return ""
        avg = sum(p.get("scoville", 0) for p in self._products) / len(self._products)
        return f"\n  SHU MEDIU CATALOG: {avg:,.0f}"
