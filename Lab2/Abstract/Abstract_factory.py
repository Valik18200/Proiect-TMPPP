from abc import ABC, abstractmethod


# ─────────────────────────────────────────
#  PRODUSE ABSTRACTE
# ─────────────────────────────────────────

class Sauce(ABC):
    @abstractmethod
    def get_description(self) -> str:
        pass

    def __str__(self) -> str:
        return self.get_description()


class SpiceBlend(ABC):
    @abstractmethod
    def get_description(self) -> str:
        pass

    def __str__(self) -> str:
        return self.get_description()


class PepperSample(ABC):
    @abstractmethod
    def get_description(self) -> str:
        pass

    def __str__(self) -> str:
        return self.get_description()


# ─────────────────────────────────────────
#  NIVEL MILD (pana la 5.000 SHU)
# ─────────────────────────────────────────

class MildSauce(Sauce):
    def get_description(self) -> str:
        return "Sos Sweet Chili Citric, 500ml — 1.500 SHU (potrivit pentru incepatori)"


class MildSpiceBlend(SpiceBlend):
    def get_description(self) -> str:
        return "Amestec Cajun usor, 250g — 3.000 SHU (aromat, nu iute)"


class MildPepperSample(PepperSample):
    def get_description(self) -> str:
        return "Ardei Ancho deshidratati intregi — 2.000 SHU (dulceag si afumat)"


# ─────────────────────────────────────────
#  NIVEL MEDIUM (5.000 – 50.000 SHU)
# ─────────────────────────────────────────

class MediumSauce(Sauce):
    def get_description(self) -> str:
        return "Sos Sriracha Original, 250ml — 2.200 SHU / Chipotle Afumat, 250ml — 3.500 SHU"


class MediumSpiceBlend(SpiceBlend):
    def get_description(self) -> str:
        return "Cayenne Pudra, 100g — 40.000 SHU (clasic si versatil)"


class MediumPepperSample(PepperSample):
    def get_description(self) -> str:
        return "Ardei Jalapeno deshidratati intregi — 8.000 SHU (echilibrat)"


# ─────────────────────────────────────────
#  NIVEL INFERNO (peste 50.000 SHU)
# ─────────────────────────────────────────

class InfernoSauce(Sauce):
    def get_description(self) -> str:
        return "Sos Ghost Pepper Inferno, 100ml — 100.000 SHU (doar pentru curajosi!)"


class InfernoSpiceBlend(SpiceBlend):
    def get_description(self) -> str:
        return "Fulgi Ardei Bird's Eye, 50g — 100.000 SHU (atentie extrema!)"


class InfernoPepperSample(PepperSample):
    def get_description(self) -> str:
        return "Carolina Reaper Pudra, 30g — 2.200.000 SHU (cel mai iute ardei din lume!)"


# ─────────────────────────────────────────
#  FABRICA ABSTRACTA
# ─────────────────────────────────────────

class HeatLevelPackageFactory(ABC):
    """
    Fabrica abstracta ce creaza un pachet complet de produse iuti
    corespunzator unui nivel de iuteala (Mild / Medium / Inferno).
    """

    @abstractmethod
    def create_sauce(self) -> Sauce:
        pass

    @abstractmethod
    def create_spice_blend(self) -> SpiceBlend:
        pass

    @abstractmethod
    def create_pepper_sample(self) -> PepperSample:
        pass

    def create_package(self) -> dict:
        return {
            "sauce":         self.create_sauce(),
            "spice_blend":   self.create_spice_blend(),
            "pepper_sample": self.create_pepper_sample(),
        }


# ─────────────────────────────────────────
#  FABRICI CONCRETE
# ─────────────────────────────────────────

class MildPackageFactory(HeatLevelPackageFactory):
    """
    Pachet pentru incepatori — arome placute, iuteala minima.
    Ideal pentru cei care vor sa descopere lumea condimentelor fara riscuri.
    """
    def create_sauce(self) -> Sauce:
        return MildSauce()

    def create_spice_blend(self) -> SpiceBlend:
        return MildSpiceBlend()

    def create_pepper_sample(self) -> PepperSample:
        return MildPepperSample()


class MediumPackageFactory(HeatLevelPackageFactory):
    """
    Pachet pentru cunoscatori — iuteala echilibrata si arome complexe.
    Potrivit pentru cei cu experienta in condimente.
    """
    def create_sauce(self) -> Sauce:
        return MediumSauce()

    def create_spice_blend(self) -> SpiceBlend:
        return MediumSpiceBlend()

    def create_pepper_sample(self) -> PepperSample:
        return MediumPepperSample()


class InfernoPackageFactory(HeatLevelPackageFactory):
    """
    Pachet pentru aventurieri — iuteala extrema, nu pentru inimi slabe!
    Recomandat doar celor cu toleranta ridicata la capsaicina.
    """
    def create_sauce(self) -> Sauce:
        return InfernoSauce()

    def create_spice_blend(self) -> SpiceBlend:
        return InfernoSpiceBlend()

    def create_pepper_sample(self) -> PepperSample:
        return InfernoPepperSample()
