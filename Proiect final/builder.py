from abc import ABC, abstractmethod


class SpiceGiftBox:
    def __init__(self):
        self.product_name = None
        self.wrapping = None
        self.ribbon = None
        self.card_message = None
        self.extras = []

    def __str__(self):
        parts = ["Pachet cadou ARDEI ROSU:"]
        parts.append(f"  Produs:     {self.product_name}")
        parts.append(f"  Ambalaj:    {self.wrapping}")
        parts.append(f"  Panglica:   {self.ribbon}")
        parts.append(f"  Felicitare: {self.card_message}")
        if self.extras:
            parts.append(f"  Extras:     {', '.join(self.extras)}")
        return "\n".join(parts)


class SpiceGiftBoxBuilder(ABC):
    def __init__(self):
        self._box = SpiceGiftBox()

    @abstractmethod
    def set_product(self):
        pass

    @abstractmethod
    def set_wrapping(self):
        pass

    @abstractmethod
    def set_ribbon(self):
        pass

    @abstractmethod
    def set_card(self):
        pass

    @abstractmethod
    def add_extras(self):
        pass

    def get_box(self) -> SpiceGiftBox:
        return self._box


class HotLoversBoxBuilder(SpiceGiftBoxBuilder):
    """Pachet pentru pasionatii de iuteala extrema."""

    def set_product(self):
        self._box.product_name = "Ghost Pepper Inferno 100ml + Carolina Reaper Pudra 30g"
        return self

    def set_wrapping(self):
        self._box.wrapping = "Cutie neagra cu flacari rosii"
        return self

    def set_ribbon(self):
        self._box.ribbon = "Panglica rosie cu ardei imprimate"
        return self

    def set_card(self):
        self._box.card_message = "Pentru cei cu adevarat curajosi! 🌶️🔥"
        return self

    def add_extras(self):
        self._box.extras = ["Manusi de protectie", "Card avertisment iuteala", "Servetel racoritor"]
        return self


class GourmetSpiceBoxBuilder(SpiceGiftBoxBuilder):
    """Pachet gourmet pentru cunoscatorii de arome fine."""

    def set_product(self):
        self._box.product_name = "Sriracha Original 250ml + Amestec Cajun 250g + Sare Roz cu Chili 150g"
        return self

    def set_wrapping(self):
        self._box.wrapping = "Cutie kraft cu design rustic"
        return self

    def set_ribbon(self):
        self._box.ribbon = "Panglica bej cu eticheta manuala"
        return self

    def set_card(self):
        self._box.card_message = "O calatorie culinara prin lumea condimentelor!"
        return self

    def add_extras(self):
        self._box.extras = ["Reteta recomandata", "Mini catalog produse", "Esantion nou produs"]
        return self


class StarterKitBoxBuilder(SpiceGiftBoxBuilder):
    """Pachet de introducere pentru incepatori — iuteala usoara."""

    def set_product(self):
        self._box.product_name = "Sweet Chili Citric 500ml + Ardei Ancho deshidratati"
        return self

    def set_wrapping(self):
        self._box.wrapping = "Punga de hartie reciclata cu imprimeu ardei"
        return self

    def set_ribbon(self):
        self._box.ribbon = "Fara panglica"
        return self

    def set_card(self):
        self._box.card_message = "Bun venit in lumea condimentelor! Incepe usor 🌿"
        return self

    def add_extras(self):
        self._box.extras = ["Ghid incepator iuteala", "Scara Scoville imprimata"]
        return self


class SpiceDirector:
    def __init__(self, builder: SpiceGiftBoxBuilder):
        self._builder = builder

    def build_full_box(self) -> SpiceGiftBox:
        self._builder.set_product()
        self._builder.set_wrapping()
        self._builder.set_ribbon()
        self._builder.set_card()
        self._builder.add_extras()
        return self._builder.get_box()

    def build_minimal_box(self) -> SpiceGiftBox:
        self._builder.set_product()
        self._builder.set_wrapping()
        return self._builder.get_box()
