from typing import List

from classes.locker import LockerMediator, Locker
from classes.parcel import Parcel
from classes.storage import StorageFacility


# Courier Class
class Courier:
    def __init__(self, name, intermediate_store: StorageFacility, external_storage: StorageFacility, mediator: LockerMediator):
        self.name = name
        self.intermediate_store = intermediate_store
        self.external_storage = external_storage
        self.mediator = mediator

    def transfer_parcel_to_intermediate(self, from_locker: Locker, parcel_id: str):
        parcel = from_locker.dispatch_parcel(parcel_id)
        if parcel:
            self.intermediate_store.store_parcel(parcel)
            self.notify_user(parcel, f"Parcel {parcel_id} transferred to intermediate storage.")
        else:
            print("Failed to transfer parcel to intermediate store.")

    def transfer_parcel_from_intermediate(self, to_locker: Locker, parcel_id: str):
        parcel = self.intermediate_store.retrieve_parcel(parcel_id)
        if parcel:
            if not to_locker.receive_parcel(parcel):
                print("Failed to deposit parcel in locker from intermediate store.")
                self.intermediate_store.store_parcel(parcel)
            else:
                self.notify_user(parcel, f"Parcel {parcel_id} transferred from intermediate storage to locker {to_locker.identifier}.")

    def move_to_external_storage(self, parcel_id: str):
        parcel = self.intermediate_store.retrieve_parcel(parcel_id)
        if parcel:
            self.external_storage.store_parcel(parcel)
            self.notify_user(parcel, f"Parcel {parcel_id} moved to external storage.")

    def transfer_parcel(self, from_location, to_location, parcel_id: str):
        if isinstance(from_location, Locker):
            parcel = from_location.dispatch_parcel(parcel_id)
        else:
            parcel = from_location.retrieve_parcel(parcel_id)

        if parcel:
            if isinstance(to_location, Locker):
                if not to_location.receive_parcel(parcel):
                    print("Failed to deposit parcel. No available slot in destination locker.")
                    if isinstance(from_location, Locker):
                        from_location.receive_parcel(parcel)
                    else:
                        from_location.store_parcel(parcel)
                else:
                    self.notify_user(parcel, f"Parcel {parcel_id} transferred from {from_location.__class__.__name__} to locker {to_location.identifier}.")
            else:
                to_location.store_parcel(parcel)
                self.notify_user(parcel, f"Parcel {parcel_id} transferred from {from_location.__class__.__name__} to storage {to_location.name}.")
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

    def notify_user(self, parcel: Parcel, message: str):
        print(f"Notification to {parcel.recipient.name}: {message}")

