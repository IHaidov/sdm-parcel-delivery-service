from abc import ABC, abstractmethod


# Visitor Pattern
class Visitor(ABC):
    @abstractmethod
    def visit(self, element):
        pass

class ParcelReportVisitor(Visitor):
    def visit(self, parcel: 'Parcel'):
        print(f"Parcel ID: {parcel.identifier}, Status: {parcel.payment_status}")
        print(f"Sender: {parcel.sender.name}, Recipient: {parcel.recipient.name}")

class LockerReportVisitor(Visitor):
    def visit(self, locker: 'Locker'):
        print(f"Locker ID: {locker.identifier}, Address: {locker.address}")
        for slot in locker.slots:
            status = "occupied" if slot.is_occupied else "free"
            print(f"  Slot Size: {slot.size}, Status: {status}")

class StorageReportVisitor(Visitor):
    def visit(self, storage: 'StorageFacility'):
        print(f"Storage Name: {storage.name}")
        if storage.storage:
            print(f"Storage Contents:")
            for parcel_id in storage.storage:
                print(f"- Parcel ID: {parcel_id}")
        else:
            print("Storage is currently empty.")

