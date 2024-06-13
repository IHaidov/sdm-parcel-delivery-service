from typing import Optional

from classes.parcel import Parcel
from visitor import Visitor


# Storage Facility Class
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

    def accept(self, visitor: Visitor):
        visitor.visit(self)

