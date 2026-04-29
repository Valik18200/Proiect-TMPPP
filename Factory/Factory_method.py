from abc import ABC, abstractmethod


# ─────────────────────────────────────────
#  CLASA DE BAZA PRODUS
# ─────────────────────────────────────────

class SpiceProduct(ABC):
    def __init__(self, name: str, price: float, scoville: int):
        self._name = name
        self._price = price
        self._scoville = scoville

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    @property
    def scoville(self) -> int:
        return self._scoville

    @abstractmethod
    def get_description(self) -> str:
        pass

    def __str__(self) -> str:
        return f"{self._name} - {self._price:.2f} LEI | {self._scoville} SHU | {self.get_description()}"


# ─────────────────────────────────────────
#  PRODUSE CONCRETE
# ─────────────────────────────────────────

class HotSauce(SpiceProduct):
    def __init__(self, name: str, price: float, scoville: int,
                 flavor: str, volume_ml: int):
        super().__init__(name, price, scoville)
        self._flavor = flavor
        self._volume_ml = volume_ml

    @property
    def flavor(self) -> str:
        return self._flavor

    @property
    def volume_ml(self) -> int:
        return self._volume_ml

    def get_description(self) -> str:
        return f"Sos iute cu aroma {self._flavor}, {self._volume_ml}ml"


class Spice(SpiceProduct):
    def __init__(self, name: str, price: float, scoville: int,
                 form: str, weight_g: int):
        super().__init__(name, price, scoville)
        self._form = form
        self._weight_g = weight_g

    @property
    def form(self) -> str:
        return self._form

    @property
    def weight_g(self) -> int:
        return self._weight_g

    def get_description(self) -> str:
        return f"Condiment {self._form}, {self._weight_g}g"


class DriedPepper(SpiceProduct):
    def __init__(self, name: str, price: float, scoville: int,
                 variety: str, whole: bool):
        super().__init__(name, price, scoville)
        self._variety = variety
        self._whole = whole

    @property
    def variety(self) -> str:
        return self._variety

    @property
    def whole(self) -> bool:
        return self._whole

    def get_description(self) -> str:
        forma = "intregi" if self._whole else "macinati"
        return f"Ardei deshidratati {self._variety}, {forma}"


class HotSalt(SpiceProduct):
    def __init__(self, name: str, price: float, scoville: int,
                 base_salt: str, weight_g: int):
        super().__init__(name, price, scoville)
        self._base_salt = base_salt
        self._weight_g = weight_g

    @property
    def base_salt(self) -> str:
        return self._base_salt

    @property
    def weight_g(self) -> int:
        return self._weight_g

    def get_description(self) -> str:
        return f"Sare iute pe baza de {self._base_salt}, {self._weight_g}g"


# ─────────────────────────────────────────
#  FABRICA DE BAZA (Factory Method)
# ─────────────────────────────────────────

class SpiceProductFactory(ABC):
    @abstractmethod
    def create_product(self) -> SpiceProduct:
        pass

    def order_product(self) -> SpiceProduct:
        product = self.create_product()
        print(f"  Produs creat: {product}")
        return product


# ─────────────────────────────────────────
#  FABRICI CONCRETE
# ─────────────────────────────────────────

class SrirachaFactory(SpiceProductFactory):
    """Fabrica pentru sosul clasic Sriracha."""
    def create_product(self) -> SpiceProduct:
        return HotSauce("Sriracha Original", 39.99, 2200, "clasic", 250)


class HabaneroMangoFactory(SpiceProductFactory):
    """Fabrica pentru sosul Habanero Mango."""
    def create_product(self) -> SpiceProduct:
        return HotSauce("Habanero Mango Blast", 54.99, 8000, "mango", 150)


class GhostPepperSauceFactory(SpiceProductFactory):
    """Fabrica pentru sosul Ghost Pepper - pentru cei curajos."""
    def create_product(self) -> SpiceProduct:
        return HotSauce("Ghost Pepper Inferno", 69.99, 100000, "habanero", 100)


class CayennePowderFactory(SpiceProductFactory):
    """Fabrica pentru pudra de Cayenne."""
    def create_product(self) -> SpiceProduct:
        return Spice("Cayenne Pudra", 24.99, 40000, "pudra", 100)


class CajunBlendFactory(SpiceProductFactory):
    """Fabrica pentru amestecul Cajun."""
    def create_product(self) -> SpiceProduct:
        return Spice("Amestec Cajun", 29.99, 5000, "granule", 250)


class JalapenoWholePepperFactory(SpiceProductFactory):
    """Fabrica pentru ardei Jalapeno deshidratati intregi."""
    def create_product(self) -> SpiceProduct:
        return DriedPepper("Jalapeno Intreg", 27.99, 8000, "jalapeno", True)


class CarolinaReaperFactory(SpiceProductFactory):
    """Fabrica pentru pudra Carolina Reaper - cel mai iute ardei din lume."""
    def create_product(self) -> SpiceProduct:
        return DriedPepper("Carolina Reaper Pudra", 79.99, 2200000, "carolina reaper", False)


class PinkHimalayaSaltFactory(SpiceProductFactory):
    """Fabrica pentru sare roz himalaya cu chili."""
    def create_product(self) -> SpiceProduct:
        return HotSalt("Sare Roz cu Chili", 18.99, 5000, "roz himalaya", 150)



