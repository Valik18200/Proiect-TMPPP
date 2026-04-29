# facade.py
class InventoryService:
    def __init__(self):
        self._stock = {
            "Sos Habanero Extreme": 15,
            "Sos Carolina Reaper": 8,
            "Sos Ghost Pepper": 12,
            "Ardei iuti uscati": 25,
            "Pudra de ardei iute": 30,
            "Sos Jalapeno Classic": 20,
        }

    def check_availability(self, product_name: str) -> bool:
        return self._stock.get(product_name, 0) > 0

    def reserve(self, product_name: str) -> bool:
        if self._stock.get(product_name, 0) > 0:
            self._stock[product_name] -= 1
            return True
        return False


class PricingService:
    PRICES = {
        "Sos Habanero Extreme": 34.99,
        "Sos Carolina Reaper": 49.99,
        "Sos Ghost Pepper": 44.99,
        "Ardei iuti uscati": 19.99,
        "Pudra de ardei iute": 15.99,
        "Sos Jalapeno Classic": 24.99,
    }

    def get_price(self, product_name: str) -> float:
        return self.PRICES.get(product_name, 0.0)

    def apply_discount(self, price: float, discount: float) -> float:
        return price * (1 - discount)


class PaymentService:
    def process_payment(self, amount: float) -> str:
        return f"Plata de {amount:.2f} LEI procesata cu succes"


class NotificationService:
    def send_confirmation(self, product_name: str, total: float) -> str:
        return f"Email trimis: Ati comandat '{product_name}' - {total:.2f} LEI"


class GiftWrappingService:
    def pack(self, product_name: str, gift_pack: bool) -> str:
        if gift_pack:
            return f"'{product_name}' a fost ambalat cadou in cutie speciala Ardeirosu"
        return f"'{product_name}' in punga standard de magazin"


class OrderFacade:
    def __init__(self):
        self._inventory = InventoryService()
        self._pricing = PricingService()
        self._payment = PaymentService()
        self._notification = NotificationService()
        self._wrapping = GiftWrappingService()

    def place_order(self, product_name: str, discount: float = 0.0, gift_pack: bool = False) -> str:
        steps = []

        if not self._inventory.check_availability(product_name):
            return f"Eroare: '{product_name}' nu este in stoc."

        price = self._pricing.get_price(product_name)
        final_price = self._pricing.apply_discount(price, discount)
        steps.append(f"Pret: {price:.2f} LEI -> {final_price:.2f} LEI (reducere {discount*100:.0f}%)")

        self._inventory.reserve(product_name)
        steps.append("Stoc actualizat")

        steps.append(self._payment.process_payment(final_price))
        steps.append(self._wrapping.pack(product_name, gift_pack))
        steps.append(self._notification.send_confirmation(product_name, final_price))

        return "\n    ".join(steps)