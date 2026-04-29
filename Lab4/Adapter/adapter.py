# adapter.py
from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass


class PayPalAPI:
    def make_payment(self, email: str, total: float) -> str:
        return f"PayPal: platit {total:.2f} LEI de pe contul {email}"


class StripeAPI:
    def charge(self, token: str, amount_cents: int) -> str:
        return f"Stripe: incasat {amount_cents} bani (token: {token})"


class CashRegister:
    def process_cash(self, received: float, price: float) -> str:
        rest = received - price
        return f"Cash: primit {received:.2f} LEI, rest {rest:.2f} LEI"


class PayPalAdapter(PaymentProcessor):
    def __init__(self, email: str):
        self._paypal = PayPalAPI()
        self._email = email

    def pay(self, amount: float) -> str:
        return self._paypal.make_payment(self._email, amount)


class StripeAdapter(PaymentProcessor):
    def __init__(self, token: str):
        self._stripe = StripeAPI()
        self._token = token

    def pay(self, amount: float) -> str:
        amount_cents = int(amount * 100)
        return self._stripe.charge(self._token, amount_cents)


class CashAdapter(PaymentProcessor):
    def __init__(self, received: float):
        self._cash = CashRegister()
        self._received = received

    def pay(self, amount: float) -> str:
        return self._cash.process_cash(self._received, amount)