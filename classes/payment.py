from classes.parcel import Parcel
from tariffs import TariffStrategy


# Payment Class
class Payment:
    base_prices = {'S': 5, 'M': 8, 'L': 10}

    def __init__(self, parcel: Parcel, tariff_strategy: TariffStrategy):
        self.parcel = parcel
        self.tariff_strategy = tariff_strategy

    def calculate_total(self):
        total = self.base_prices.get(self.parcel.size, 0)
        total = self.tariff_strategy.calculate_fee(total)
        return total

    def process_payment(self):
        total = self.calculate_total()
        print(f"Total payment due for parcel {self.parcel.identifier}: ${total}")
        self.parcel.update_payment_status('Paid')
        print(f"Payment processed for parcel {self.parcel.identifier}.")
        print(f"Temporary Human-Friendly Code: {self.parcel.temp_code}")
        self.parcel.calculate_delivery_times(base_days=3 if self.parcel.services.get('priority') else 5)



