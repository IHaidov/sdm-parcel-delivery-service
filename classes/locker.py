from collections import deque
from classes.event import Event
from classes.parcel import Parcel
from classes.slot import Slot
from datetime import datetime


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
