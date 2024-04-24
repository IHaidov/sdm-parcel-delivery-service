import datetime

from Common.models import Parcel


class ConsoleInterface:
    def __init__(self, parcel_service, locker_service, event_service, payment_service):
        self.parcel_service = parcel_service
        self.locker_service = locker_service
        self.event_service = event_service
        self.payment_service = payment_service

    def start(self):
        while True:
            print("Welcome to the Parcel Delivery Service!")
            print("1. Register Parcel")
            print("2. View Parcel")
            print("3. Exit")
            choice = input("Choose an option: ")

            if choice == '1':
                self.register_parcel()
            elif choice == '2':
                self.view_parcel()
            elif choice == '3':
                print("Exiting...")
                break
            else:
                print("Invalid option. Please try again.")

    def register_parcel(self):
        # Example interaction
        sender_id = input("Enter sender ID: ")
        recipient_id = input("Enter recipient ID: ")
        size = input("Enter size (S, M, L): ")
        # Assume parcel ID is auto-generated in reality and other details are handled
        self.parcel_service.register_parcel(Parcel(id=None, sender_id=sender_id, recipient_id=recipient_id, size=size, registered_time=datetime.date.today(), delivery_time=None, pick_up_time=None))
        print("Parcel registered successfully.")

    def view_parcel(self):
        parcel_id = input("Enter parcel ID to view: ")
        parcel = self.parcel_service.get_parcel_info(parcel_id)
        if parcel:
            parcel_id, sender_id, recipient_id, registered_time, delivery_time, pick_up_time, size = parcel
            print(f"Parcel ID: {parcel_id}, Size: {size}")

            # print(f"Parcel ID: {parcel.id}, Size: {parcel.size}, Status: {parcel.status}")
        else:
            print("Parcel not found.")
