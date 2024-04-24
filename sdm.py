import sys
from datetime import datetime
from typing import List, Optional

class User:
    def __init__(self, name: str, contact_info: str, address: str):
        self.name = name
        self.contact_info = contact_info
        self.address = address

class Event:
    def __init__(self, timestamp: datetime, location: str, event_type: str):
        self.timestamp = timestamp
        self.location = location
        self.type = event_type

class Parcel:
    def __init__(self, sender: User, recipient: User, size: str, services: Optional[dict] = None):
        self.sender = sender
        self.recipient = recipient
        self.size = size
        self.identifier = self.generate_id()
        self.services = services or {}
        self.transit_history = []
        self.payment_status = 'Pending'

    def generate_id(self):
        import uuid
        return str(uuid.uuid4())

    def add_event(self, event: Event):
        self.transit_history.append(event)

    def update_payment_status(self, status: str):
        self.payment_status = status

class Payment:
    base_prices = {'S': 5, 'M': 8, 'L': 10}  # example base prices for sizes

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
        # Here you would typically interface with a payment gateway
        self.parcel.update_payment_status('Paid')
        print(f"Payment processed for parcel {self.parcel.identifier}.")

class Slot:
    def __init__(self, size: str):
        self.size = size
        self.is_occupied = False
        self.current_parcel = None

    def occupy(self, parcel: Parcel):
        self.current_parcel = parcel
        self.is_occupied = True
        self.add_event(Event(datetime.now(), f"Slot sized {self.size}", "Occupied"))

    def vacate(self):
        self.add_event(Event(datetime.now(), f"Slot sized {self.size}", "Vacated"))
        self.current_parcel = None
        self.is_occupied = False

    def add_event(self, event: Event):
        if self.current_parcel:
            self.current_parcel.add_event(event)

class Locker:
    def __init__(self, identifier: str, address: str):
        self.identifier = identifier
        self.address = address
        self.slots = []

    def add_slot(self, slot: Slot):
        self.slots.append(slot)

    def receive_parcel(self, parcel):
        if parcel.payment_status != 'Paid':
            print(f"Cannot deposit parcel {parcel.identifier} without payment.")
            return False
        for slot in self.slots:
            if not slot.is_occupied and slot.size == parcel.size:
                slot.occupy(parcel)
                event = Event(datetime.now(), self.address, "Parcel Deposited")
                parcel.add_event(event)
                return True
        print("No available slot for this parcel.")
        return False


    def dispatch_parcel(self, parcel_id: str):
        for slot in self.slots:
            if slot.is_occupied and slot.current_parcel.identifier == parcel_id:
                parcel = slot.current_parcel
                slot.vacate()
                event = Event(datetime.now(), self.address, "Parcel Dispatched")
                return parcel
        return None

    def list_lockers(self, locker_system):
        print("\nAvailable Lockers:")
        for locker in locker_system:
            print(
                f"Locker ID: {locker.identifier}, Address: {locker.address}, Available Slots: {len([slot for slot in locker.slots if not slot.is_occupied])}")


class Courier:
    def __init__(self, name: str):
        self.name = name

    def transfer_parcel(self, from_locker: Locker, to_locker: Locker, parcel_id: str):
        parcel = from_locker.dispatch_parcel(parcel_id)
        if parcel:
            if not to_locker.receive_parcel(parcel):
                print("Failed to deposit parcel. No available slot in destination locker.")
                from_locker.receive_parcel(parcel)  # Return to original locker
            else:
                print(f"Parcel {parcel_id} transferred from {from_locker.address} to {to_locker.address}")
        else:
            print("Parcel not found or already collected.")

    def show_locker_details(self, locker_system):
        print("\nLocker Details:")
        for locker in locker_system:
            print(f"\nLocker ID: {locker.identifier}, Address: {locker.address}")
            for slot in locker.slots:
                slot_status = "Taken" if slot.is_occupied else "Free"
                current_parcel = slot.current_parcel.identifier if slot.is_occupied else "None"
                print(f"  Slot Size: {slot.size}, Status: {slot_status}, Parcel ID: {current_parcel}")


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
            print("5. Courier Actions")
            print("6. View Lockers")
            print("7. Exit")
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
                self.courier_menu()
            elif choice == '6':
                self.view_lockers_ui()
            elif choice == '7':
                print("Exiting system.")
                sys.exit(0)
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")

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
        # UI logic for collecting a parcel
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
        # UI logic for tracking a parcel
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
