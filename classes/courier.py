from classes.locker import Locker


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
