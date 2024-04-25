import sys
from collections import deque
from datetime import datetime, timedelta
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
        self.estimated_delivery_time = None
        self.actual_delivery_time = None
        self.guaranteed_delivery_time = None
        self.actual_pick_up_time = None

    def generate_id(self):
        import uuid
        return str(uuid.uuid4())

    def add_event(self, event: Event):
        self.transit_history.append(event)

    def update_payment_status(self, status: str):
        self.payment_status = status

    def get_details(self):
        details = {
            "Parcel ID": self.identifier,
            "Sender": self.sender.name,
            "Recipient": self.recipient.name,
            "Size": self.size,
            "Services": ", ".join([k for k, v in self.services.items() if v]),
            "Payment Status": self.payment_status
        }
        return details

    def calculate_delivery_times(self, base_days: int):
        self.estimated_delivery_time = datetime.now() + timedelta(days=base_days)
        self.guaranteed_delivery_time = self.estimated_delivery_time + timedelta(days=2)  # 2 days buffer

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
            "Estimated Delivery Time": self.estimated_delivery_time.strftime(
                "%Y-%m-%d %H:%M:%S") if self.estimated_delivery_time else "Not Set",
            "Actual Delivery Time": self.actual_delivery_time.strftime(
                "%Y-%m-%d %H:%M:%S") if self.actual_delivery_time else "Not Delivered",
            "Guaranteed Delivery Time": self.guaranteed_delivery_time.strftime(
                "%Y-%m-%d %H:%M:%S") if self.guaranteed_delivery_time else "Not Set",
            "Actual Pick Up Time": self.actual_pick_up_time.strftime(
                "%Y-%m-%d %H:%M:%S") if self.actual_pick_up_time else "Not Picked Up"
        }
        for key, value in times.items():
            print(f"{key}: {value}")

    def get_transit_history(self):
        return [{"Timestamp": event.timestamp.strftime("%Y-%m-%d %H:%M:%S"), "Location": event.location,
                 "Event": event.type} for event in self.transit_history]


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
            self.current_parcel.record_pick_up()  # Record the pick-up time
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
        self.parcel_history = deque(maxlen=7)  # Store last 7 days of parcel activity
        self.expected_parcels = []

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
                parcel.record_delivery()
                self.parcel_history.append((parcel.identifier, datetime.now(), "Deposited"))
                return True
        print("No available slot for this parcel.")
        return False


    def dispatch_parcel(self, parcel_id: str):
        for slot in self.slots:
            if slot.is_occupied and slot.current_parcel.identifier == parcel_id:
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
        # Assuming a simple check that counts slots and expected parcels for a specific future date
        occupied = sum(1 for slot in self.slots if slot.is_occupied)
        expected = len(self.expected_parcels)
        total_slots = len(self.slots)
        available_slots = total_slots - occupied - expected
        print(f"On {date_time.strftime('%Y-%m-%d')}, available slots: {available_slots}")


    def list_lockers(self, locker_system):
        print("\nAvailable Lockers:")
        for locker in locker_system:
            print(
                f"Locker ID: {locker.identifier}, Address: {locker.address}, Available Slots: {len([slot for slot in locker.slots if not slot.is_occupied])}")

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
