from DataAccessLayer.locker_repository import LockerRepository

class LockerService:
    def __init__(self, locker_repository: LockerRepository):
        self.locker_repository = locker_repository

    def add_new_locker(self, locker):
        self.locker_repository.add_locker(locker)

    def retrieve_locker_details(self, locker_id):
        return self.locker_repository.get_locker(locker_id)
