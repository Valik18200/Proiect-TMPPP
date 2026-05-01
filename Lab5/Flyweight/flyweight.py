class HotPepperType:
    def __init__(self, category: str, heat_level: str, origin: str):
        self.category = category  # Ardei iute, Sos iute, Paste iute, etc.
        self.heat_level = heat_level  # Scoville: Mild, Mediu, Picant, Extra-Picant, Inferno
        self.origin = origin  # Romania, Mexic, India, Tailanda, etc.

    def __str__(self):
        return f"[{self.category}, Scoville: {self.heat_level}, Origine: {self.origin}]"


class HotPepperTypeFactory:
    _types: dict = {}

    @classmethod
    def get_pepper_type(cls, category: str, heat_level: str, origin: str) -> HotPepperType:
        key = f"{category}_{heat_level}_{origin}"
        if key not in cls._types:
            cls._types[key] = HotPepperType(category, heat_level, origin)
        return cls._types[key]

    @classmethod
    def get_count(cls) -> int:
        return len(cls._types)

    @classmethod
    def clear(cls):
        cls._types.clear()


class ProductOnShelf:
    def __init__(self, name: str, price: float, pepper_type: HotPepperType):
        self.name = name
        self.price = price
        self.pepper_type = pepper_type

    def display(self) -> str:
        return f"🌶️ {self.name} - {self.price:.2f} LEI {self.pepper_type}"