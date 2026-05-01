# observer.py
from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self, event: str, data: dict):
        pass


class Subject:
    def __init__(self):
        self._observers: list[Observer] = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, event: str, data: dict):
        for obs in self._observers:
            obs.update(event, data)


class HotSauceStore(Subject):
    def new_product(self, sauce_name: str, price: float, scoville: int):
        self.notify("new_product", {"sauce": sauce_name, "price": price, "scoville": scoville})

    def price_drop(self, sauce_name: str, old_price: float, new_price: float):
        self.notify("price_drop", {"sauce": sauce_name, "old": old_price, "new": new_price})

    def back_in_stock(self, sauce_name: str):
        self.notify("back_in_stock", {"sauce": sauce_name})

    def spicy_challenge(self, sauce_name: str, scoville: int):
        self.notify("spicy_challenge", {"sauce": sauce_name, "scoville": scoville})


class EmailSubscriber(Observer):
    def __init__(self, email: str):
        self.email = email
        self.messages = []

    def update(self, event: str, data: dict):
        if event == "new_product":
            msg = f"[Email -> {self.email}] 🌶️ PRODUS NOU la Ardeirosu: {data['sauce']} - {data['price']:.2f} LEI (Scoville: {data['scoville']:,} SHU)"
        elif event == "price_drop":
            msg = f"[Email -> {self.email}] 🔥 REDUCERE: {data['sauce']} {data['old']:.2f} -> {data['new']:.2f} LEI"
        elif event == "back_in_stock":
            msg = f"[Email -> {self.email}] ✅ {data['sauce']} a revenit in stoc!"
        elif event == "spicy_challenge":
            msg = f"[Email -> {self.email}] ⚠️ NOUL PROVOCARE: {data['sauce']} - {data['scoville']:,} SHU!"
        else:
            msg = f"[Email -> {self.email}] {event}: {data}"
        self.messages.append(msg)


class SMSSubscriber(Observer):
    def __init__(self, phone: str):
        self.phone = phone
        self.messages = []

    def update(self, event: str, data: dict):
        if event == "price_drop":
            msg = f"[SMS -> {self.phone}] 🔥 OFERTA ARDEIROSU: {data['sauce']} acum {data['new']:.2f} LEI!"
        elif event == "spicy_challenge":
            msg = f"[SMS -> {self.phone}] ⚠️ ATENTIE! {data['sauce']} - {data['scoville']:,} SHU! Provocare iuteala maxima!"
        else:
            msg = f"[SMS -> {self.phone}] {event}: {data}"
        self.messages.append(msg)


class DashboardLogger(Observer):
    def __init__(self):
        self.log = []

    def update(self, event: str, data: dict):
        self.log.append({"event": event, "data": data, "timestamp": len(self.log)})