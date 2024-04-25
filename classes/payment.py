class Payment:
    base_prices = {'S': 5, 'M': 8, 'L': 10}

    def __init__(self, parcel):
        self.parcel = parcel

    def calculate_total(self):
        total = self.base_prices.get(self.parcel.size, 0)
        for service, active in self.parcel.services.items():
            if active:
                if service == 'insurance':
                    total += 2
                elif service == 'priority':
                    total += 5
                elif service == 'extended_storage':
                    total += 1
        return total

    def process_payment(self):
        total = self.calculate_total()
        print(f"Total payment due for parcel {self.parcel.identifier}: ${total}")
        self.parcel.update_payment_status('Paid')
        print(f"Payment processed for parcel {self.parcel.identifier}.")
        self.parcel.calculate_delivery_times(base_days=3 if 'priority' in self.parcel.services and self.parcel.services['priority'] else 5)
