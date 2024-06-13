# SDM Parcel Delivery Service

## Table of Contents
- [Introduction](#introduction)
- [Design Patterns Used](#design-patterns-used)
- [Requirements & Installation](#requirements--installation)
- [Usage](#usage)

## Introduction

The SDM Parcel Delivery Service is a project designed to efficiently manage the delivery of parcels from one location to another. It aims to streamline the process of delivering parcels by providing a centralized system for managing parcel requests, tracking deliveries, and optimizing routes. The service offers a user-friendly interface for both customers and delivery personnel. Additionally, it utilizes various design patterns to enhance the modularity, flexibility, and maintainability of the codebase.

## Design Patterns Used

### 1. Strategy Pattern

The Strategy Pattern is used to define a family of algorithms, encapsulate each one, and make them interchangeable. This pattern is implemented in the `TariffStrategy` class and its subclasses (`RegularTariff`, `PriorityTariff`, and `ExtendedStorageTariff`). Each subclass implements the `calculate_fee` method, providing different fee calculation strategies.

```python
from abc import ABC, abstractmethod

class TariffStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, base_price: float) -> float:
        pass

class RegularTariff(TariffStrategy):
    def calculate_fee(self, base_price: float) -> float:
        return base_price

class PriorityTariff(TariffStrategy):
    def calculate_fee(self, base_price: float) -> float:
        return base_price * 1.2

class ExtendedStorageTariff(TariffStrategy):
    def calculate_fee(self, base_price: float) -> float:
        return base_price + 5
```

### 2. Visitor Pattern

The Visitor Pattern is used to add further operations to objects without modifying them. It is implemented in the `Visitor` class and its subclasses (`ParcelReportVisitor`, `LockerReportVisitor`, and `StorageReportVisitor`). These visitors perform operations on objects (`Parcel`, `Locker`, and `StorageFacility`) by accepting visitors.

```python
from abc import ABC, abstractmethod

class Visitor(ABC):
    @abstractmethod
    def visit(self, element):
        pass

class ParcelReportVisitor(Visitor):
    def visit(self, parcel: 'Parcel'):
        print(f"Parcel ID: {parcel.identifier}, Status: {parcel.payment_status}")

class LockerReportVisitor(Visitor):
    def visit(self, locker: 'Locker'):
        print(f"Locker ID: {locker.identifier}, Address: {locker.address}")

class StorageReportVisitor(Visitor):
    def visit(self, storage: 'StorageFacility'):
        print(f"Storage Name: {storage.name}")
```

### 3. Command Pattern

The Command Pattern is used to encapsulate a request as an object, thereby allowing for parameterization and queuing of requests. This pattern is implemented in the `Command` class and its subclasses (`RegisterParcelCommand`, `PayParcelCommand`, `DepositParcelCommand`, and `CollectParcelCommand`). Each subclass defines an `execute` method to perform specific actions.

```python
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

class PayParcelCommand(Command):
    def __init__(self, parcel: 'Parcel', payment: 'Payment'):
        self.parcel = parcel
        self.payment = payment

    def execute(self):
        print(f"Processing payment for parcel {self.parcel.identifier}")
        self.payment.process_payment()
```

### 4. Composite Pattern

The Composite Pattern is used to compose objects into tree structures to represent part-whole hierarchies. This pattern allows clients to treat individual objects and compositions uniformly. It is implemented in the `LockerComponent` class, `LockerComposite`, and `Locker`.

```python
from abc import ABC, abstractmethod

class LockerComponent(ABC):
    @abstractmethod
    def operation(self):
        pass

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

    def operation(self):
        print(f"Locker {self.identifier} at {self.address}")
        for slot in self.slots:
            status = "occupied" if slot.is_occupied else "free"
            print(f"  Slot Size: {slot.size}, Status: {status}")
```

### 5. Mediator Pattern

The Mediator Pattern is used to reduce chaotic dependencies between objects by introducing a mediator object. This pattern is implemented in the `LockerMediator` class, which handles communication between lockers and storage facilities.

```python
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
```

### Summary

- **Strategy Pattern:** Implemented for different fee calculation strategies using `TariffStrategy` and its subclasses.
- **Visitor Pattern:** Implemented for different reporting operations using `Visitor` and its subclasses.
- **Command Pattern:** Implemented for various parcel-related operations using `Command` and its subclasses.
- **Composite Pattern:** Implemented for creating a hierarchical structure of lockers using `LockerComponent`, `LockerComposite`, and `Locker`.
- **Mediator Pattern:** Implemented to facilitate communication between lockers and storage facilities using `LockerMediator`.

## Requirements & Installation

To install and run the SDM Parcel Delivery Service, follow these steps:

1. Ensure Python 3 is installed on your PC.
2. Clone the repository: 
   ```sh
   git clone https://github.com/IHaidov/sdm-parcel-delivery-service.git
   ```
3. Navigate to the project directory:
   ```sh
   cd sdm-parcel-delivery-service
   ```

## Usage

To start the SDM Parcel Delivery Service, run the following command in the terminal:

```sh
python main.py
```

This will launch the application and provide instructions on how to interact with it.

---