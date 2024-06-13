# Command Pattern
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class RegisterParcelCommand(Command):
    def __init__(self, parcel: 'Parcel'):
        self.parcel = parcel

    def execute(self):
        print(f"Registering parcel {self.parcel.identifier}")
        # Registration logic here


class PayParcelCommand(Command):
    def __init__(self, parcel: 'Parcel', payment: 'Payment'):
        self.parcel = parcel
        self.payment = payment

    def execute(self):
        print(f"Processing payment for parcel {self.parcel.identifier}")
        self.payment.process_payment()


class DepositParcelCommand(Command):
    def __init__(self, locker: 'Locker', parcel: 'Parcel'):
        self.locker = locker
        self.parcel = parcel

    def execute(self):
        self.locker.receive_parcel(self.parcel)


class CollectParcelCommand(Command):
    def __init__(self, locker: 'Locker', parcel_id: str):
        self.locker = locker
        self.parcel_id = parcel_id

    def execute(self):
        self.locker.dispatch_parcel(self.parcel_id)
