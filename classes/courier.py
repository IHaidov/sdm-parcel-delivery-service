from classes.locker import Locker


class Courier:
    def __init__(self, name, intermediate_store, external_storage):
        self.name = name
        self.intermediate_store = intermediate_store
        self.external_storage = external_storage

    def transfer_parcel_to_intermediate(self, from_locker, parcel_id):
        parcel = from_locker.dispatch_parcel(parcel_id)
        if parcel:
            self.intermediate_store.store_parcel(parcel)
        else:
            print("Failed to transfer parcel to intermediate store.")

    def transfer_parcel_from_intermediate(self, to_locker, parcel_id):
        parcel = self.intermediate_store.retrieve_parcel(parcel_id)
        if parcel:
            if not to_locker.receive_parcel(parcel):
                print("Failed to deposit parcel in locker from intermediate store.")
                self.intermediate_store.store_parcel(parcel)  # Store back if deposit fails

    def move_to_external_storage(self, parcel_id):
        parcel = self.intermediate_store.retrieve_parcel(parcel_id)
        if parcel:
            self.external_storage.store_parcel(parcel)
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
