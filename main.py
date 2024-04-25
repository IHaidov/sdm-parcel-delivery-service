import sys
from datetime import datetime
from typing import List
from classes.courier import Courier
from classes.locker import Locker
from classes.parcel import Parcel
from classes.payment import Payment
from classes.slot import Slot
from classes.user import User


class UserInterface:
    def __init__(self, locker_system: List[Locker], courier: Courier):
        self.locker_system = locker_system
        self.courier = courier

    def main_menu(self):
        while True:
            print("\nMain Menu")
            print("1. Register and Pay for a Parcel")
            print("2. Deposit a Parcel")
            print("3. Collect a Parcel")
            print("4. Track a Parcel")
            print("5. View Parcel Information")
            print("6. Courier Actions")
            print("7. Locker Actions")
            print("8. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.register_and_pay_for_parcel()
            elif choice == '2':
                self.deposit_parcel_ui()
            elif choice == '3':
                self.collect_parcel_ui()
            elif choice == '4':
                self.track_parcel_ui()
            elif choice == '5':
                self.view_parcel_info_ui()
            elif choice == '6':
                self.courier_menu()
            elif choice == '7':
                self.locker_management_menu()
            elif choice == '8':
                print("Exiting system.")
                sys.exit(0)
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")

    def locker_management_menu(self):
        while True:
            print("\nLocker Management Menu")
            print("1. Update Locker Details")
            print("2. View All Lockers")
            print("3. Check Locker Availability")
            print("4. Return to Main Menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.update_locker_ui()
            elif choice == '2':
                self.view_lockers_ui()
            elif choice == '3':
                self.check_locker_availability_ui()
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")

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
                self.courier.show_locker_details(self.locker_system)
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

    def update_locker_ui(self):
        print("Update Locker Details")
        locker_id = input("Enter locker ID: ")
        new_id = input("Enter new locker ID: ")
        new_address = input("Enter new locker address: ")
        locker = next((l for l in self.locker_system if l.identifier == locker_id), None)
        if locker:
            locker.update_details(new_id, new_address)
        else:
            print("Locker not found.")

    def check_locker_availability_ui(self):
        locker_id = input("Enter locker ID: ")
        date_str = input("Enter date (YYYY-MM-DD): ")
        date_time = datetime.strptime(date_str, "%Y-%m-%d")
        locker = next((l for l in self.locker_system if l.identifier == locker_id), None)
        if locker:
            locker.check_availability(date_time)
        else:
            print("Locker not found.")

    def view_parcel_info_ui(self):
        parcel_id = input("Enter the parcel ID to view details: ")
        for locker in self.locker_system:
            for slot in locker.slots:
                if slot.is_occupied and slot.current_parcel.identifier == parcel_id:
                    info = slot.current_parcel.get_details()
                    for key, value in info.items():
                        print(f"{key}: {value}")
                    slot.current_parcel.display_parcel_times()
                    return
        print("Parcel not found.")

    def view_parcel_history_ui(self):
        parcel_id = input("Enter the parcel ID to view history: ")
        for locker in self.locker_system:
            for slot in locker.slots:
                if slot.is_occupied and slot.current_parcel.identifier == parcel_id:
                    history = slot.current_parcel.get_transit_history()
                    if history:
                        for event in history:
                            print(
                                f"Timestamp: {event['Timestamp']}, Location: {event['Location']}, Event: {event['Event']}")
                        return
                    else:
                        print("No history available for this parcel.")
                        return
        print("Parcel not found.")

    def transfer_parcel_ui(self):
        from_locker_id = input("Enter from locker ID: ")
        to_locker_id = input("Enter to locker ID: ")
        parcel_id = input("Enter parcel ID to transfer: ")
        from_locker = next((locker for locker in self.locker_system if locker.identifier == from_locker_id), None)
        to_locker = next((locker for locker in self.locker_system if locker.identifier == to_locker_id), None)
        if from_locker and to_locker:
            self.courier.transfer_parcel(from_locker, to_locker, parcel_id)
        else:
            print("Invalid locker ID(s) provided.")

    def register_and_pay_for_parcel(self):
        self.view_lockers_ui()
        locker_id = input("Choose a locker ID for your parcel: ")
        locker = next((l for l in self.locker_system if l.identifier == locker_id), None)
        if not locker:
            print("Invalid locker ID.")
            return
        sender_name = input("Enter sender name: ")
        recipient_name = input("Enter recipient name: ")
        size = input("Enter parcel size (L, M, S): ")
        services = {
            'insurance': input("Add insurance? (yes/no): ").lower() == 'yes',
            'priority': input("Add priority shipping? (yes/no): ").lower() == 'yes',
            'extended_storage': input("Add extended storage? (yes/no): ").lower() == 'yes'
        }
        sender = User(sender_name, "sender@example.com", "Sender Address")
        recipient = User(recipient_name, "recipient@example.com", "Recipient Address")
        parcel = Parcel(sender, recipient, size, services)
        payment = Payment(parcel)
        payment.process_payment()
        if locker.receive_parcel(parcel):
            print(f"Parcel {parcel.identifier} has been successfully deposited in locker {locker.identifier}.")
        else:
            print("Failed to deposit parcel; no available slots.")

    def view_lockers_ui(self):
        for locker in self.locker_system:
            print(f"Locker ID: {locker.identifier}, Address: {locker.address}")
            for slot in locker.slots:
                status = "occupied" if slot.is_occupied else "free"
                print(f"    Slot Size: {slot.size}, Status: {status}")

    def try_to_deposit_parcel(self, parcel):
        for locker in self.locker_system:
            if locker.receive_parcel(parcel):
                print(f"Parcel {parcel.identifier} has been successfully deposited in locker {locker.identifier}.")
                return
        print("Failed to deposit parcel; no available slots.")

    def deposit_parcel_ui(self):
        parcel_id = input("Enter the parcel ID to deposit: ")
        for locker in self.locker_system:
            for slot in locker.slots:
                if slot.current_parcel and slot.current_parcel.identifier == parcel_id:
                    if locker.receive_parcel(slot.current_parcel):
                        print(f"Parcel {parcel_id} deposited successfully.")
                        return
        print("Parcel not found or no available slot.")

    def collect_parcel_ui(self):
        parcel_id = input("Enter the parcel ID to collect: ")
        found = False
        for locker in self.locker_system:
            parcel = locker.dispatch_parcel(parcel_id)
            if parcel:
                found = True
                print(f"Parcel {parcel_id} collected successfully.")
                break
        if not found:
            print("Parcel not found.")

    def track_parcel_ui(self):
        parcel_id = input("Enter the parcel ID to track: ")
        found = False
        for locker in self.locker_system:
            for slot in locker.slots:
                if slot.is_occupied and slot.current_parcel.identifier == parcel_id:
                    found = True
                    print(f"Tracking Parcel {parcel_id}:")
                    for event in slot.current_parcel.transit_history:
                        print(f"- {event.type} at {event.timestamp} in location {event.location}")
                    break
        if not found:
            print("Parcel not found.")


# Setup for demonstration
locker1 = Locker("123", "123 Street, City A")
locker2 = Locker("456", "456 Road, City B")
locker1.add_slot(Slot("L"))
locker1.add_slot(Slot("M"))
locker2.add_slot(Slot("L"))
locker2.add_slot(Slot("S"))
locker_system = [locker1, locker2]
courier = Courier("John Doe")

ui = UserInterface(locker_system, courier)
ui.main_menu()
