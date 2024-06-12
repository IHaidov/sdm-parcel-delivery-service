'''V1.5.2 temporary code disappears after transfer fix'''
import sys
from datetime import datetime, timedelta
from typing import List, Optional
import uuid
import random
import string


class Event:
    def __init__(self, timestamp: datetime, location: str, event_type: str):
        self.timestamp = timestamp
        self.location = location
        self.type = event_type


class User:
    def __init__(self, name: str, contact_info: str, address: str, phone_number: str):
        self.name = name
        self.contact_info = contact_info
        self.address = address
        self.phone_number = phone_number


class Parcel:
    def __init__(self, sender: User, recipient: User, size: str, sender_locker: str, delivery_locker: str, services: Optional[dict] = None):
        self.sender = sender
        self.recipient = recipient
        self.size = size
        self.identifier = self.generate_id()
        self.temp_code = None
        self.sender_locker = sender_locker
        self.delivery_locker = delivery_locker
        self.services = services or {}
        self.transit_history = []
        self.payment_status = 'Pending'
        self.estimated_delivery_time = None
        self.actual_delivery_time = None
        self.guaranteed_delivery_time = None
        self.actual_pick_up_time = None

    def generate_id(self):
        return str(uuid.uuid4())

    def generate_temp_code(self):
        self.temp_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def clear_temp_code(self):
        self.temp_code = None

    def add_event(self, event: Event):
        self.transit_history.append(event)

    def update_payment_status(self, status: str):
        self.payment_status = status
        if status == 'Paid':
            self.generate_temp_code()

    def get_details(self):
        details = {
            "Parcel ID": self.identifier,
            "Temporary Code": self.temp_code,
            "Sender Name": self.sender.name,
            "Sender Phone": self.sender.phone_number,
            "Recipient Name": self.recipient.name,
            "Recipient Phone": self.recipient.phone_number,
            "Sender Locker": self.sender_locker,
            "Delivery Locker": self.delivery_locker,
            "Size": self.size,
            "Services": ", ".join([k for k, v in self.services.items() if v]),
            "Payment Status": self.payment_status
        }
        return details

    def calculate_delivery_times(self, base_days: int):
        self.estimated_delivery_time = datetime.now() + timedelta(days=base_days)
        self.guaranteed_delivery_time = self.estimated_delivery_time + timedelta(days=2)

    def record_delivery(self):
        self.actual_delivery_time = datetime.now()
        event = Event(self.actual_delivery_time, "Destination Locker", "Parcel Delivered")
        self.add_event(event)

    def record_pick_up(self):
        self.actual_pick_up_time = datetime.now()
        event = Event(self.actual_pick_up_time, "Destination Locker", "Parcel Picked Up")
        self.add_event(event)

    def display_parcel_times(self):
        times = {
            "Estimated Delivery Time": self.estimated_delivery_time.strftime("%Y-%m-%d %H:%M:%S") if self.estimated_delivery_time else "Not Set",
            "Actual Delivery Time": self.actual_delivery_time.strftime("%Y-%m-%d %H:%M:%S") if self.actual_delivery_time else "Not Delivered",
            "Guaranteed Delivery Time": self.guaranteed_delivery_time.strftime("%Y-%m-%d %H:%M:%S") if self.guaranteed_delivery_time else "Not Set",
            "Actual Pick Up Time": self.actual_pick_up_time.strftime("%Y-%m-%d %H:%M:%S") if self.actual_pick_up_time else "Not Picked Up"
        }
        for key, value in times.items():
            print(f"{key}: {value}")

    def get_transit_history(self):
        return [{"Timestamp": event.timestamp.strftime("%Y-%m-%d %H:%M:%S"), "Location": event.location, "Event": event.type} for event in self.transit_history]


class Payment:
    base_prices = {'S': 5, 'M': 8, 'L': 10}

    def __init__(self, parcel: Parcel):
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
        print(f"Temporary Human-Friendly Code: {self.parcel.temp_code}")
        self.parcel.calculate_delivery_times(base_days=3 if self.parcel.services.get('priority') else 5)


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
        if self.current_parcel:
            self.current_parcel.record_pick_up()
        event = Event(datetime.now(), f"Slot sized {self.size}", "Vacated")
        self.current_parcel.add_event(event)
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
        self.parcel_history = []
        self.expected_parcels = []

    def add_slot(self, slot: Slot):
        self.slots.append(slot)

    def receive_parcel(self, parcel: Parcel):
        if parcel.payment_status != 'Paid':
            print(f"Cannot deposit parcel {parcel.identifier} without payment.")
            return False
        for slot in self.slots:
            if not slot.is_occupied and slot.size == parcel.size:
                slot.occupy(parcel)
                event = Event(datetime.now(), self.address, "Parcel Deposited")
                parcel.add_event(event)
                parcel.record_delivery()
                self.parcel_history.append((parcel.identifier, datetime.now(), "Deposited"))
                return True
        print("No available slot for this parcel.")
        return False

    def dispatch_parcel(self, parcel_id: str):
        for slot in self.slots:
            if slot.is_occupied and (slot.current_parcel.identifier == parcel_id or slot.current_parcel.temp_code == parcel_id):
                parcel = slot.current_parcel
                slot.vacate()
                event = Event(datetime.now(), self.address, "Parcel Dispatched")
                self.parcel_history.append((parcel_id, datetime.now(), "Dispatched"))
                return parcel
        return None

    def add_expected_parcel(self, parcel: Parcel):
        self.expected_parcels.append(parcel)

    def remove_expected_parcel(self, parcel_id: str):
        self.expected_parcels = [p for p in self.expected_parcels if p.identifier != parcel_id]

    def check_availability(self, date_time: datetime):
        occupied = sum(1 for slot in self.slots if slot.is_occupied)
        expected = len(self.expected_parcels)
        total_slots = len(self.slots)
        available_slots = total_slots - occupied - expected
        print(f"On {date_time.strftime('%Y-%m-%d')}, available slots: {available_slots}")

    def update_details(self, new_identifier: str, new_address: str):
        if self.can_update_details():
            self.identifier = new_identifier
            self.address = new_address
            print(f"Locker details updated to ID {self.identifier}, Address {self.address}")
        else:
            print("Cannot update details. Locker is not empty or has incoming parcels.")

    def can_update_details(self):
        if any(slot.is_occupied for slot in self.slots) or self.expected_parcels:
            return False
        return True


class StorageFacility:
    def __init__(self, name):
        self.name = name
        self.storage = {}

    def store_parcel(self, parcel: Parcel):
        self.storage[parcel.identifier] = parcel
        print(f"Parcel {parcel.identifier} stored in {self.name}.")

    def retrieve_parcel(self, parcel_id: str) -> Optional[Parcel]:
        if parcel_id in self.storage:
            parcel = self.storage.pop(parcel_id)
            print(f"Parcel {parcel_id} retrieved from {self.name}.")
            return parcel
        else:
            print(f"Parcel {parcel_id} not found in {self.name}.")
            return None

    def view_storage(self):
        if self.storage:
            print(f"{self.name} Contents:")
            for parcel_id in self.storage:
                print(f"- Parcel ID: {parcel_id}")
        else:
            print(f"{self.name} is currently empty.")


class Courier:
    def __init__(self, name, intermediate_store: StorageFacility, external_storage: StorageFacility):
        self.name = name
        self.intermediate_store = intermediate_store
        self.external_storage = external_storage

    def transfer_parcel_to_intermediate(self, from_locker: Locker, parcel_id: str):
        parcel = from_locker.dispatch_parcel(parcel_id)
        if parcel:
            self.intermediate_store.store_parcel(parcel)
        else:
            print("Failed to transfer parcel to intermediate store.")

    def transfer_parcel_from_intermediate(self, to_locker: Locker, parcel_id: str):
        parcel = self.intermediate_store.retrieve_parcel(parcel_id)
        if parcel:
            if not to_locker.receive_parcel(parcel):
                print("Failed to deposit parcel in locker from intermediate store.")
                self.intermediate_store.store_parcel(parcel)

    def move_to_external_storage(self, parcel_id: str):
        parcel = self.intermediate_store.retrieve_parcel(parcel_id)
        if parcel:
            self.external_storage.store_parcel(parcel)

    def transfer_parcel(self, from_locker: Locker, to_locker: Locker, parcel_id: str):
        parcel = from_locker.dispatch_parcel(parcel_id)
        if parcel:
            if not to_locker.receive_parcel(parcel):
                print("Failed to deposit parcel. No available slot in destination locker.")
                from_locker.receive_parcel(parcel)
            else:
                print(f"Parcel {parcel_id} transferred from {from_locker.address} to {to_locker.address}")
        else:
            print("Parcel not found or already collected.")

    def show_locker_details(self, locker_system: List[Locker]):
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
        for locker in self.locker_system:
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

    def register_parcel(self):
        self.view_lockers_ui()
        sender_name = input("Enter sender name: ")
        sender_phone = input("Enter sender phone number: ")
        recipient_name = input("Enter recipient name: ")
        recipient_phone = input("Enter recipient phone number: ")
        size = input("Enter parcel size (L, M, S): ")
        sender_locker = input("Enter sender locker ID: ")
        delivery_locker = input("Enter delivery locker ID: ")
        sender_locker_obj = next((l for l in self.locker_system if l.identifier == sender_locker), None)
        delivery_locker_obj = next((l for l in self.locker_system if l.identifier == delivery_locker), None)
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
            payment = Payment(parcel)
            payment.process_payment()
            self.notify_user(parcel, "Payment completed successfully.")
        else:
            print("Parcel not found or already paid.")

    def view_lockers_ui(self):
        for locker in self.locker_system:
            print(f"Locker ID: {locker.identifier}, Address: {locker.address}")
            for slot in locker.slots:
                status = "occupied" if slot.is_occupied else "free"
                print(f"    Slot Size: {slot.size}, Status: {status}")

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
        sender_locker = next((l for l in self.locker_system if l.identifier == parcel.sender_locker), None)
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
            for locker in self.locker_system:
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
        for locker in self.locker_system:
            for slot in locker.slots:
                if slot.is_occupied and (slot.current_parcel.identifier == parcel_id or slot.current_parcel.temp_code == parcel_id):
                    return slot.current_parcel
        for locker in self.locker_system:
            for parcel in locker.expected_parcels:
                if parcel.identifier == parcel_id or parcel.temp_code == parcel_id:
                    return parcel
        return None

    def notify_user(self, parcel: Parcel, message: str):
        print(f"Notification to {parcel.recipient.name}: {message}")


# Setup for demonstration
intermediate_store = StorageFacility("Intermediate Store")
external_storage = StorageFacility("External Storage")
courier = Courier("John Doe", intermediate_store, external_storage)

locker1 = Locker("123", "123 Street, City A")
locker2 = Locker("456", "456 Road, City B")

# Adding slots to lockers
locker1.add_slot(Slot("L"))
locker1.add_slot(Slot("S"))
locker1.add_slot(Slot("M"))
locker1.add_slot(Slot("M"))
locker2.add_slot(Slot("L"))
locker2.add_slot(Slot("S"))
locker2.add_slot(Slot("M"))
locker2.add_slot(Slot("L"))

locker_system = [locker1, locker2]

ui = UserInterface(locker_system, courier)
ui.main_menu()
