from abc import ABC, abstractmethod


# Strategy Pattern
class TariffStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, base_price: float) -> float:
        pass


class RegularTariff(TariffStrategy):
    def calculate_fee(self, base_price: float) -> float:
        return base_price


class PriorityTariff(TariffStrategy):
    def calculate_fee(self, base_price: float) -> float:
        return base_price * 1.2


class ExtendedStorageTariff(TariffStrategy):
    def calculate_fee(self, base_price: float) -> float:
        return base_price + 5
