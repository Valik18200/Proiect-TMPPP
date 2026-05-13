class SpiceType:
    """
    Stare intrinseca (partajata) — caracteristici comune mai multor produse.
    Categoria, forma si intensitatea iutelii sunt aceleasi pentru produse similare.
    """
    def __init__(self, category: str, form: str, heat_level: str):
        self.category   = category    # ex: "sos_iute", "condiment", "ardei", "sare"
        self.form       = form        # ex: "lichid", "pudra", "fulgi", "intreg"
        self.heat_level = heat_level  # ex: "mild", "medium", "hot", "inferno"

    def __str__(self):
        return f"[{self.category} | {self.form} | {self.heat_level}]"


class SpiceTypeFactory:
    """
    Flyweight Factory — returneaza instanta existenta sau creeaza una noua.
    Toate produsele cu aceeasi categorie+forma+heat_level impart acelasi SpiceType.
    """
    _types: dict = {}

    @classmethod
    def get_spice_type(cls, category: str, form: str, heat_level: str) -> SpiceType:
        key = f"{category}_{form}_{heat_level}"
        if key not in cls._types:
            cls._types[key] = SpiceType(category, form, heat_level)
        return cls._types[key]

    @classmethod
    def get_count(cls) -> int:
        return len(cls._types)

    @classmethod
    def clear(cls):
        cls._types.clear()


class SpiceOnShelf:
    """
    Stare extrinseca (unica per instanta) — numele si pretul sunt specifice
    fiecarui produs in parte; tipul este partajat prin flyweight.
    """
    def __init__(self, name: str, price: float, scoville: int, spice_type: SpiceType):
        self.name        = name
        self.price       = price
        self.scoville    = scoville
        self.spice_type  = spice_type

    def display(self) -> str:
        return (f"{self.name} - {self.price:.2f} LEI "
                f"| {self.scoville} SHU {self.spice_type}")
