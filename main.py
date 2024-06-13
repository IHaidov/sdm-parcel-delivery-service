import sys
from datetime import datetime, timedelta
from typing import List, Optional
from abc import ABC, abstractmethod
import uuid
import random
import string

from classes.courier import Courier
from classes.locker import LockerMediator, Locker, LockerComposite
from classes.slot import Slot
from classes.storage import StorageFacility
from ui.user_interface import UserInterface

# Setup for demonstration
intermediate_store = StorageFacility("Intermediate Store")
external_storage = StorageFacility("External Storage")
mediator = LockerMediator()
courier = Courier("John Doe", intermediate_store, external_storage, mediator)

locker1 = Locker("123", "123 Street, City A")
locker2 = Locker("456", "456 Road, City B")
mediator.register_locker(locker1)
mediator.register_locker(locker2)
mediator.register_storage(intermediate_store)
mediator.register_storage(external_storage)

# Adding slots to lockers
locker1.add_slot(Slot("L"))
locker1.add_slot(Slot("S"))
locker1.add_slot(Slot("M"))
locker1.add_slot(Slot("M"))
locker2.add_slot(Slot("L"))
locker2.add_slot(Slot("S"))
locker2.add_slot(Slot("M"))
locker2.add_slot(Slot("L"))

locker_system = LockerComposite()
locker_system.add(locker1)
locker_system.add(locker2)

ui = UserInterface(locker_system, courier)
ui.main_menu()
