from abc import ABC, abstractmethod


class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> str:
        pass


class BasicNotification(Notification):
    def __init__(self, recipient: str):
        self._recipient = recipient

    def send(self, message: str) -> str:
        return f"Notificare catre {self._recipient}: {message}"


class NotificationDecorator(Notification):
    def __init__(self, wrapped: Notification):
        self._wrapped = wrapped

    def send(self, message: str) -> str:
        return self._wrapped.send(message)


class EmailDecorator(NotificationDecorator):
    def send(self, message: str) -> str:
        base = super().send(message)
        return f"{base}\n    📧 Email trimis cu oferta iute!"


class SMSDecorator(NotificationDecorator):
    def send(self, message: str) -> str:
        base = super().send(message)
        return f"{base}\n    📱 SMS trimis cu recomandare picanta!"


class PushDecorator(NotificationDecorator):
    def send(self, message: str) -> str:
        base = super().send(message)
        return f"{base}\n    🔔 Push notification: Stoc nou de ardei iuti!"


class SpicyPackDecorator(NotificationDecorator):
    def send(self, message: str) -> str:
        base = super().send(message)
        return f"{base}\n    🔥 Pachet gratuit de ardei iute proaspat adaugat!"