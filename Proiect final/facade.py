# ─────────────────────────────────────────
#  SUBSISTEME (complexe, nu sunt expuse direct clientului)
# ─────────────────────────────────────────

class SpiceInventoryService:
    def __init__(self):
        self._stock = {
            "Sriracha Original":          30,
            "Ghost Pepper Inferno":       10,
            "Cayenne Pudra":              40,
            "Jalapeno Intreg":            25,
            "Sare Roz cu Chili":          45,
            "Habanero Mango Blast":       20,
            "Carolina Reaper Pudra":       8,
            "Amestec Cajun":              30,
        }

    def check_availability(self, product_name: str) -> bool:
        return self._stock.get(product_name, 0) > 0

    def reserve(self, product_name: str) -> bool:
        if self._stock.get(product_name, 0) > 0:
            self._stock[product_name] -= 1
            return True
        return False

    def get_stock(self, product_name: str) -> int:
        return self._stock.get(product_name, 0)


class SpicePricingService:
    PRICES = {
        "Sriracha Original":          39.99,
        "Ghost Pepper Inferno":       69.99,
        "Cayenne Pudra":              24.99,
        "Jalapeno Intreg":            27.99,
        "Sare Roz cu Chili":          18.99,
        "Habanero Mango Blast":       54.99,
        "Carolina Reaper Pudra":      79.99,
        "Amestec Cajun":              29.99,
    }

    SCOVILLE = {
        "Sriracha Original":           2_200,
        "Ghost Pepper Inferno":      100_000,
        "Cayenne Pudra":              40_000,
        "Jalapeno Intreg":             8_000,
        "Sare Roz cu Chili":           5_000,
        "Habanero Mango Blast":        8_000,
        "Carolina Reaper Pudra":   2_200_000,
        "Amestec Cajun":               5_000,
    }

    def get_price(self, product_name: str) -> float:
        return self.PRICES.get(product_name, 0.0)

    def get_scoville(self, product_name: str) -> int:
        return self.SCOVILLE.get(product_name, 0)

    def apply_discount(self, price: float, discount: float) -> float:
        return price * (1 - discount)


class SpicePaymentService:
    def process_payment(self, amount: float) -> str:
        return f"Plata de {amount:.2f} LEI procesata cu succes"


class SpiceNotificationService:
    def send_confirmation(self, product_name: str, total: float, scoville: int) -> str:
        warning = ""
        if scoville >= 100_000:
            warning = " ⚠️  ATENTIE: produs cu iuteala extrema!"
        return (f"Email trimis: Ati comandat '{product_name}' - "
                f"{total:.2f} LEI ({scoville} SHU){warning}")


class SpicePackagingService:
    def pack(self, product_name: str, gift_wrap: bool) -> str:
        if gift_wrap:
            return f"'{product_name}' ambalat in cutie cadou cu ardei imprimat 🌶️"
        return f"'{product_name}' ambalat standard cu protectie anti-scurgere"


# ─────────────────────────────────────────
#  FACADE — interfata simplificata
# ─────────────────────────────────────────

class SpiceOrderFacade:
    """
    Orchestreaza 5 subsisteme intr-un singur apel place_order().
    Clientul nu interactioneaza direct cu niciunul dintre subsisteme.
    """

    def __init__(self):
        self._inventory    = SpiceInventoryService()
        self._pricing      = SpicePricingService()
        self._payment      = SpicePaymentService()
        self._notification = SpiceNotificationService()
        self._packaging    = SpicePackagingService()

    def place_order(self, product_name: str,
                    discount: float = 0.0,
                    gift_wrap: bool = False) -> str:
        steps = []

        # 1. Verificare stoc
        if not self._inventory.check_availability(product_name):
            return f"Eroare: '{product_name}' nu este in stoc."

        # 2. Calcul pret
        price = self._pricing.get_price(product_name)
        scoville = self._pricing.get_scoville(product_name)
        final_price = self._pricing.apply_discount(price, discount)
        steps.append(
            f"Pret: {price:.2f} LEI -> {final_price:.2f} LEI "
            f"(reducere {discount*100:.0f}%) | {scoville} SHU"
        )

        # 3. Rezervare stoc
        self._inventory.reserve(product_name)
        steps.append("Stoc actualizat")

        # 4. Procesare plata
        steps.append(self._payment.process_payment(final_price))

        # 5. Ambalare
        steps.append(self._packaging.pack(product_name, gift_wrap))

        # 6. Notificare
        steps.append(self._notification.send_confirmation(product_name, final_price, scoville))

        return "\n    ".join(steps)
