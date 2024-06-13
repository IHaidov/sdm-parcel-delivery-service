# User Interface Class
import sys
from datetime import datetime
from typing import Optional

from classes.courier import Courier
from classes.locker import LockerComposite, Locker
from classes.parcel import Parcel
from classes.payment import Payment
from classes.slot import Slot
from classes.storage import StorageFacility
from classes.user import User
from commands.commands import PayParcelCommand
from tariffs import RegularTariff
from visitor import StorageReportVisitor


class UserInterface:
    def __init__(self, locker_system: LockerComposite, courier: Courier):
        self.locker_system = locker_system
        self.courier = courier

    def main_menu(self):
        while True:
            print("\nMain Menu")
            print("1. Register a Parcel")
            print("2. Pay for a Parcel")
            print("3. Deposit a Parcel")
            print("4. Collect a Parcel")
            print("5. Track a Parcel")
            print("6. View Parcel Information")
            print("7. Courier Actions")
            print("8. Locker Actions")
            print("9. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.register_parcel()
            elif choice == '2':
                self.pay_for_parcel()
            elif choice == '3':
                self.deposit_parcel_ui()
            elif choice == '4':
                self.collect_parcel_ui()
            elif choice == '5':
                self.track_parcel_ui()
            elif choice == '6':
                self.view_parcel_info_ui()
            elif choice == '7':
                self.courier_menu()
            elif choice == '8':
                self.locker_management_menu()
            elif choice == '9':
                print("Exiting system.")
                sys.exit(0)
            else:
                print("Invalid choice. Please enter a number between 1 and 9.")

    def locker_management_menu(self):
        while True:
            print("\nLocker Management Menu")
            print("1. Update Locker Details")
            print("2. View All Lockers")
            print("3. Check Locker Availability")
            print("4. Create New Storage")
            print("5. View All Storages")
            print("6. Return to Main Menu")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.update_locker_ui()
            elif choice == '2':
                self.view_lockers_ui()
            elif choice == '3':
                self.check_locker_availability_ui()
            elif choice == '4':
                self.create_new_storage_ui()
            elif choice == '5':
                self.view_all_storages_ui()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

    def courier_menu(self):
        while True:
            print("\nCourier Menu")
            print("1. Transfer a Parcel")
            print("2. Show Locker Details")
            print("3. Return to Main Menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.transfer_parcel_ui()
            elif choice == '2':
                self.courier.show_locker_details(self.locker_system.children)
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

    def update_locker_ui(self):
        print("Update Locker Details")
        locker_id = input("Enter locker ID: ")
        new_id = input("Enter new locker ID: ")
        new_address = input("Enter new locker address: ")
        locker = next((l for l in self.locker_system.children if l.identifier == locker_id), None)
        if locker:
            locker.update_details(new_id, new_address)
        else:
            print("Locker not found.")

    def create_new_storage_ui(self):
        print("\nCreate New Storage")
        storage_type = input("Enter storage type (locker/internal/external): ").lower()

        if storage_type == 'locker':
            self.create_locker_ui()
        elif storage_type == 'internal':
            self.create_internal_storage_ui()
        elif storage_type == 'external':
            self.create_external_storage_ui()
        else:
            print("Invalid storage type. Please enter locker, internal, or external.")

    def create_locker_ui(self):
        identifier = input("Enter locker ID: ")
        address = input("Enter locker address: ")
        locker = Locker(identifier, address)

        num_slots = int(input("Enter number of slots: "))
        for _ in range(num_slots):
            slot_size = input("Enter slot size (L, M, S): ")
            locker.add_slot(Slot(slot_size))

        self.locker_system.add(locker)
        self.courier.mediator.register_locker(locker)
        print(f"Locker {identifier} created successfully.")

    def create_internal_storage_ui(self):
        name = input("Enter internal storage name: ")
        storage = StorageFacility(name)
        self.courier.intermediate_store = storage
        self.courier.mediator.register_storage(storage)
        print(f"Internal storage {name} created successfully.")

    def create_external_storage_ui(self):
        name = input("Enter external storage name: ")
        storage = StorageFacility(name)
        self.courier.external_storage = storage
        self.courier.mediator.register_storage(storage)
        print(f"External storage {name} created successfully.")

    def check_locker_availability_ui(self):
        locker_id = input("Enter locker ID: ")
        date_str = input("Enter date (YYYY-MM-DD): ")
        date_time = datetime.strptime(date_str, "%Y-%m-%d")
        locker = next((l for l in self.locker_system.children if l.identifier == locker_id), None)
        if locker:
            locker.check_availability(date_time)
        else:
            print("Locker not found.")

    def view_parcel_info_ui(self):
        parcel_id = input("Enter the parcel ID to view details: ")
        parcel = self.find_parcel_by_id(parcel_id)
        if parcel:
            info = parcel.get_details()
            for key, value in info.items():
                print(f"{key}: {value}")
            parcel.display_parcel_times()
            if parcel.payment_status == 'Pending':
                print("This parcel is pending payment.")
                pay_now = input("Do you want to pay for this parcel now? (yes/no): ").lower()
                if pay_now == 'yes':
                    self.pay_for_parcel_by_id(parcel_id)
        else:
            print("Parcel not found.")

    def view_parcel_history_ui(self):
        parcel_id = input("Enter the parcel ID to view history: ")
        for locker in self.locker_system.children:
            for slot in locker.slots:
                if slot.is_occupied and slot.current_parcel.identifier == parcel_id:
                    history = slot.current_parcel.get_transit_history()
                    if history:
                        for event in history:
                            print(f"Timestamp: {event['Timestamp']}, Location: {event['Location']}, Event: {event['Event']}")
                        return
                    else:
                        print("No history available for this parcel.")
                        return
        print("Parcel not found.")

    def view_all_storages_ui(self):
        self.courier.mediator.accept(StorageReportVisitor())

    def transfer_parcel_ui(self):
        from_location_type = input("Enter from location type (locker/internal_storage/external_storage): ")
        to_location_type = input("Enter to location type (locker/internal_storage/external_storage): ")
        from_location_id = input("Enter from location ID: ")
        to_location_id = input("Enter to location ID: ")
        parcel_id = input("Enter parcel ID to transfer: ")

        from_location = self.get_location(from_location_type, from_location_id)
        to_location = self.get_location(to_location_type, to_location_id)

        if from_location and to_location:
            self.courier.transfer_parcel(from_location, to_location, parcel_id)
        else:
            print("Invalid location ID(s) provided.")

    def get_location(self, location_type: str, location_id: str):
        if location_type == "locker":
            return next((locker for locker in self.locker_system.children if locker.identifier == location_id), None)
        elif location_type == "internal_storage":
            return self.courier.intermediate_store
        elif location_type == "external_storage":
            return self.courier.external_storage
        return None

    def register_parcel(self):
        self.view_lockers_ui()
        sender_name = input("Enter sender name: ")
        sender_phone = input("Enter sender phone number: ")
        recipient_name = input("Enter recipient name: ")
        recipient_phone = input("Enter recipient phone number: ")
        size = input("Enter parcel size (L, M, S): ")
        sender_locker = input("Enter sender locker ID: ")
        delivery_locker = input("Enter delivery locker ID: ")
        sender_locker_obj = next((l for l in self.locker_system.children if l.identifier == sender_locker), None)
        delivery_locker_obj = next((l for l in self.locker_system.children if l.identifier == delivery_locker), None)
        if not sender_locker_obj:
            print("Invalid sender locker ID.")
            return
        if not delivery_locker_obj:
            print("Invalid delivery locker ID.")
            return
        services = {
            'insurance': input("Add insurance? (yes/no): ").lower() == 'yes',
            'priority': input("Add priority shipping? (yes/no): ").lower() == 'yes',
            'extended_storage': input("Add extended storage? (yes/no): ").lower() == 'yes'
        }
        sender = User(sender_name, "sender@example.com", "Sender Address", sender_phone)
        recipient = User(recipient_name, "recipient@example.com", "Recipient Address", recipient_phone)
        parcel = Parcel(sender, recipient, size, sender_locker, delivery_locker, services)
        print(f"Parcel {parcel.identifier} has been successfully registered.")
        self.notify_user(parcel, "Parcel registered successfully.")
        sender_locker_obj.add_expected_parcel(parcel)

        # Proposal to pay immediately after registration
        pay_now = input("Do you want to pay for this parcel now? (yes/no): ").lower()
        if pay_now == 'yes':
            self.pay_for_parcel_by_id(parcel.identifier)

    def pay_for_parcel(self):
        parcel_id = input("Enter the parcel ID to pay for: ")
        self.pay_for_parcel_by_id(parcel_id)

    def pay_for_parcel_by_id(self, parcel_id: str):
        parcel = self.find_parcel_by_id(parcel_id)
        if parcel:
            if parcel.payment_status == 'Paid':
                print("Payment already completed for this parcel.")
                return
            payment = Payment(parcel, RegularTariff())
            pay_command = PayParcelCommand(parcel, payment)
            pay_command.execute()
            self.notify_user(parcel, "Payment completed successfully.")
        else:
            print("Parcel not found or already paid.")

    def view_lockers_ui(self):
        for locker in self.locker_system.children:
            locker.operation()

    def deposit_parcel_ui(self):
        parcel_id = input("Enter the parcel ID or temporary code to deposit: ")
        sender_phone = input("Enter sender's phone number: ")
        parcel = self.find_parcel_by_id(parcel_id)
        if parcel and parcel.sender.phone_number == sender_phone:
            if parcel.payment_status != 'Paid':
                print("Payment not completed. Please complete the payment first.")
                return
            self.try_to_deposit_parcel(parcel)
        else:
            print("Parcel not found or sender's phone number does not match.")

    def try_to_deposit_parcel(self, parcel: Parcel):
        sender_locker = next((l for l in self.locker_system.children if l.identifier == parcel.sender_locker), None)
        if sender_locker and sender_locker.receive_parcel(parcel):
            print(f"Parcel {parcel.identifier} has been successfully deposited in locker {sender_locker.identifier}.")
            self.notify_user(parcel, "Parcel deposited successfully.")
        else:
            print("Failed to deposit parcel; no available slots.")

    def collect_parcel_ui(self):
        parcel_id = input("Enter the parcel ID or temporary code to collect: ")
        recipient_phone = input("Enter recipient's phone number: ")
        parcel = self.find_parcel_by_id(parcel_id)
        if parcel and parcel.recipient.phone_number == recipient_phone:
            found = False
            for locker in self.locker_system.children:
                dispatched_parcel = locker.dispatch_parcel(parcel_id)
                if dispatched_parcel:
                    parcel = dispatched_parcel
                    found = True
                    print(f"Parcel {parcel.identifier} collected successfully.")
                    parcel.clear_temp_code()
                    self.notify_user(parcel, "Parcel collected successfully.")
                    break
            if not found:
                print("Parcel not found.")
        else:
            print("Parcel not found or recipient's phone number does not match.")

    def track_parcel_ui(self):
        parcel_id = input("Enter the parcel ID or temporary code to track: ")
        parcel = self.find_parcel_by_id(parcel_id)
        if parcel:
            print(f"Tracking Parcel {parcel_id}:")
            for event in parcel.transit_history:
                print(f"- {event.type} at {event.timestamp} in location {event.location}")
        else:
            print("Parcel not found.")

    def find_parcel_by_id(self, parcel_id: str) -> Optional[Parcel]:
        for locker in self.locker_system.children:
            for slot in locker.slots:
                if slot.is_occupied and (slot.current_parcel.identifier == parcel_id or slot.current_parcel.temp_code == parcel_id):
                    return slot.current_parcel
        for locker in self.locker_system.children:
            for parcel in locker.expected_parcels:
                if parcel.identifier == parcel_id or parcel.temp_code == parcel_id:
                    return parcel
        return None

    def notify_user(self, parcel: Parcel, message: str):
        print(f"Notification to {parcel.recipient.name}: {message}")
