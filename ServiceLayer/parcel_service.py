from DataAccessLayer.parcel_repository import ParcelRepository

class ParcelService:
    def __init__(self, parcel_repository: ParcelRepository):
        self.parcel_repository = parcel_repository

    def register_parcel(self, parcel):
        # Additional logic for registration like validation can be added here
        self.parcel_repository.add_parcel(parcel)

    def get_parcel_info(self, parcel_id):
        return self.parcel_repository.get_parcel(parcel_id)

    def update_parcel_delivery(self, parcel):
        # Update delivery time and other statuses
        self.parcel_repository.update_parcel(parcel)

