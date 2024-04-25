from classes.event import Event
from classes.parcel import Parcel
from datetime import datetime


class Slot:
    def __init__(self, size: str):
        self.size = size
        self.is_occupied = False
        self.current_parcel = None

    def occupy(self, parcel: Parcel):
        self.current_parcel = parcel
        self.is_occupied = True
        self.add_event(Event(datetime.now(), f"Slot sized {self.size}", "Occupied"))

    def vacate(self):
        if self.current_parcel:
            self.current_parcel.record_pick_up()  # Record the pick-up time
        event = Event(datetime.now(), f"Slot sized {self.size}", "Vacated")
        self.current_parcel.add_event(event)
        self.current_parcel = None
        self.is_occupied = False

    def add_event(self, event: Event):
        if self.current_parcel:
            self.current_parcel.add_event(event)
