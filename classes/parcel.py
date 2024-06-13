import string
import uuid
import random
from datetime import datetime, timedelta
from typing import Optional

from classes.event import Event
from classes.user import User
from visitor import Visitor


# Parcel Class
class Parcel:
    def __init__(self, sender: User, recipient: User, size: str, sender_locker: str, delivery_locker: str, services: Optional[dict] = None):
        self.sender = sender
        self.recipient = recipient
        self.size = size
        self.identifier = self.generate_id()
        self.temp_code = None
        self.sender_locker = sender_locker
        self.delivery_locker = delivery_locker
        self.services = services or {}
        self.transit_history = []
        self.payment_status = 'Pending'
        self.estimated_delivery_time = None
        self.actual_delivery_time = None
        self.guaranteed_delivery_time = None
        self.actual_pick_up_time = None

    def generate_id(self):
        return str(uuid.uuid4())

    def generate_temp_code(self):
        self.temp_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def clear_temp_code(self):
        self.temp_code = None

    def add_event(self, event: Event):
        self.transit_history.append(event)

    def update_payment_status(self, status: str):
        self.payment_status = status
        if status == 'Paid':
            self.generate_temp_code()

    def get_details(self):
        details = {
            "Parcel ID": self.identifier,
            "Temporary Code": self.temp_code,
            "Sender Name": self.sender.name,
            "Sender Phone": self.sender.phone_number,
            "Recipient Name": self.recipient.name,
            "Recipient Phone": self.recipient.phone_number,
            "Sender Locker": self.sender_locker,
            "Delivery Locker": self.delivery_locker,
            "Size": self.size,
            "Services": ", ".join([k for k, v in self.services.items() if v]),
            "Payment Status": self.payment_status
        }
        return details

    def calculate_delivery_times(self, base_days: int):
        self.estimated_delivery_time = datetime.now() + timedelta(days=base_days)
        self.guaranteed_delivery_time = self.estimated_delivery_time + timedelta(days=2)

    def record_delivery(self):
        self.actual_delivery_time = datetime.now()
        event = Event(self.actual_delivery_time, "Destination Locker", "Parcel Delivered")
        self.add_event(event)

    def record_pick_up(self):
        self.actual_pick_up_time = datetime.now()
        event = Event(self.actual_pick_up_time, "Destination Locker", "Parcel Picked Up")
        self.add_event(event)

    def display_parcel_times(self):
        times = {
            "Estimated Delivery Time": self.estimated_delivery_time.strftime("%Y-%m-%d %H:%M:%S") if self.estimated_delivery_time else "Not Set",
            "Actual Delivery Time": self.actual_delivery_time.strftime("%Y-%m-%d %H:%M:%S") if self.actual_delivery_time else "Not Delivered",
            "Guaranteed Delivery Time": self.guaranteed_delivery_time.strftime("%Y-%m-%d %H:%M:%S") if self.guaranteed_delivery_time else "Not Set",
            "Actual Pick Up Time": self.actual_pick_up_time.strftime("%Y-%m-%d %H:%M:%S") if self.actual_pick_up_time else "Not Picked Up"
        }
        for key, value in times.items():
            print(f"{key}: {value}")

    def get_transit_history(self):
        return [{"Timestamp": event.timestamp.strftime("%Y-%m-%d %H:%M:%S"), "Location": event.location, "Event": event.type} for event in self.transit_history]

    def accept(self, visitor: Visitor):
        visitor.visit(self)

