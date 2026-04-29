import threading



    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._store_name = "ARDEI ROSU"
        self._currency = "LEI"
        self._max_discount = 0.25
        self._tax_rate = 0.19
        self._max_scoville_warning = 100_000  # SHU limita de avertisment
        self._settings = {}

    @property
    def store_name(self) -> str:
        return self._store_name

    @property
    def currency(self) -> str:
        return self._currency

    @property
    def max_discount(self) -> float:
        return self._max_discount

    @property
    def tax_rate(self) -> float:
        return self._tax_rate

    @property
    def max_scoville_warning(self) -> int:
        return self._max_scoville_warning

    def set_setting(self, key: str, value):
        self._settings[key] = value

    def get_setting(self, key: str, default=None):
        return self._settings.get(key, default)

    def __str__(self):
        return (f"SpiceStoreConfig({self._store_name}, {self._currency}, "
                f"tax={self._tax_rate*100:.0f}%, max_discount={self._max_discount*100:.0f}%, "
                f"avertisment_scoville={self._max_scoville_warning} SHU)")
