from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass


# ─────────────────────────────────────────
#  API-URI EXTERNE (incompatibile intre ele)
# ─────────────────────────────────────────

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


class CryptoWallet:
    """API extern pentru plati crypto (Bitcoin / USDT)."""
    def send_crypto(self, wallet_address: str, amount_ron: float, coin: str) -> str:
        rate = 0.000021 if coin == "BTC" else 0.22  # rate fictive
        crypto_amount = amount_ron * rate
        return (f"Crypto [{coin}]: trimis {crypto_amount:.6f} {coin} "
                f"catre {wallet_address} (echivalent {amount_ron:.2f} LEI)")


# ─────────────────────────────────────────
'  ADAPTOARE — implementeaza PaymentProcessor'
# ─────────────────────────────────────────

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


class CryptoAdapter(PaymentProcessor):
    """Adaptor pentru plati crypto — converteste interfata CryptoWallet."""
    def __init__(self, wallet_address: str, coin: str = "BTC"):
        self._wallet = CryptoWallet()
        self._wallet_address = wallet_address
        self._coin = coin

    def pay(self, amount: float) -> str:
        return self._wallet.send_crypto(self._wallet_address, amount, self._coin)
