from abc import abstractmethod, ABC
from datetime import datetime
from typing import Optional

from classes.event import Event
from classes.parcel import Parcel
from classes.slot import Slot
from classes.storage import StorageFacility
from visitor import Visitor


# Composite Pattern
class LockerComponent(ABC):
    @abstractmethod
    def operation(self):
        pass


# Locker Class
class LockerComposite(LockerComponent):
    def __init__(self):
        self.children = []

    def add(self, component: LockerComponent):
        self.children.append(component)

    def remove(self, component: LockerComponent):
        self.children.remove(component)

    def operation(self):
        for child in self.children:
            child.operation()


class Locker(LockerComponent):
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

    def operation(self):
        print(f"Locker {self.identifier} at {self.address}")
        for slot in self.slots:
            status = "occupied" if slot.is_occupied else "free"
            print(f"  Slot Size: {slot.size}, Status: {status}")

    def accept(self, visitor: Visitor):
        visitor.visit(self)

# Mediator Pattern
class LockerMediator:
    def __init__(self):
        self.lockers = []
        self.storage_facilities = []

    def register_locker(self, locker: Locker):
        self.lockers.append(locker)

    def register_storage(self, storage: StorageFacility):
        self.storage_facilities.append(storage)

    def transfer_to_storage(self, parcel_id: str, storage_name: str):
        for storage in self.storage_facilities:
            if storage.name == storage_name:
                parcel = self.find_parcel(parcel_id)
                if parcel:
                    storage.store_parcel(parcel)
                    print(f"Parcel {parcel_id} transferred to {storage_name}.")

    def find_parcel(self, parcel_id: str) -> Optional[Parcel]:
        for locker in self.lockers:
            parcel = locker.dispatch_parcel(parcel_id)
            if parcel:
                return parcel
        return None

    def accept(self, visitor: Visitor):
        for storage in self.storage_facilities:
            storage.accept(visitor)


# Mediator Pattern
class LockerMediator:
    def __init__(self):
        self.lockers = []
        self.storage_facilities = []

    def register_locker(self, locker: Locker):
        self.lockers.append(locker)

    def register_storage(self, storage: StorageFacility):
        self.storage_facilities.append(storage)

    def transfer_to_storage(self, parcel_id: str, storage_name: str):
        for storage in self.storage_facilities:
            if storage.name == storage_name:
                parcel = self.find_parcel(parcel_id)
                if parcel:
                    storage.store_parcel(parcel)
                    print(f"Parcel {parcel_id} transferred to {storage_name}.")

    def find_parcel(self, parcel_id: str) -> Optional[Parcel]:
        for locker in self.lockers:
            parcel = locker.dispatch_parcel(parcel_id)
            if parcel:
                return parcel
        return None

    def accept(self, visitor: Visitor):
        for storage in self.storage_facilities:
            storage.accept(visitor)

