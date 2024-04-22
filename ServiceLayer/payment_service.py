class PaymentService:
    def calculate_fee(self, parcel):
        # Stub for fee calculation
        base_fee = 10.00
        size_fee = {'S': 5.00, 'M': 7.50, 'L': 10.00}
        return base_fee + size_fee[parcel.size]

    def process_payment(self, parcel, payment_details):
        # Stub for processing a payment
        fee = self.calculate_fee(parcel)
        print(f"Processing payment of ${fee} for parcel {parcel.id}")
        # More logic can be added for payment validation and confirmation
