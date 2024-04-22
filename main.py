from ServiceLayer.parcel_service import ParcelService
from ServiceLayer.locker_service import LockerService
from ServiceLayer.event_service import EventService
from ServiceLayer.payment_service import PaymentService
from console_interface import ConsoleInterface
from DataAccessLayer.parcel_repository import ParcelRepository
from DataAccessLayer.locker_repository import LockerRepository
from DataAccessLayer.event_repository import EventRepository


def main():
    # Initialize repositories
    parcel_repository = ParcelRepository(db_path="path_to_db.sqlite")
    locker_repository = LockerRepository(db_path="path_to_db.sqlite")
    event_repository = EventRepository(db_path="path_to_db.sqlite")

    # Initialize services
    parcel_service = ParcelService(parcel_repository)
    locker_service = LockerService(locker_repository)
    event_service = EventService(event_repository)
    payment_service = PaymentService()

    # Start console interface
    console_interface = ConsoleInterface(parcel_service, locker_service, event_service, payment_service)
    console_interface.start()


if __name__ == '__main__':
    main()
