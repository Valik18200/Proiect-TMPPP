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
        return f"{base}\n    + Email trimis cu detalii comanda"


class SMSDecorator(NotificationDecorator):
    def send(self, message: str) -> str:
        base = super().send(message)
        return f"{base}\n    + SMS trimis cu codul de tracking"


class PushDecorator(NotificationDecorator):
    def send(self, message: str) -> str:
        base = super().send(message)
        return f"{base}\n    + Push notification trimis pe aplicatie"


class HeatWarningDecorator(NotificationDecorator):
    """Decorator specific domeniului — adauga avertisment pentru produse extrem de iuti."""
    def send(self, message: str) -> str:
        base = super().send(message)
        return (f"{base}\n    + ⚠️  AVERTISMENT IUTEALA: manipulati cu grija! "
                f"Evitati contactul cu ochii. Pastrati la indemana apa cu zahar.")
