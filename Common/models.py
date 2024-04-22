from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Parcel:
    id: int
    sender_id: int
    recipient_id: int
    registered_time: datetime
    delivery_time: Optional[datetime]
    pick_up_time: Optional[datetime]
    size: str  # Could be 'S', 'M', or 'L'

@dataclass
class Locker:
    id: int
    location: str
    slots: int
    slot_size: str  # Could be 'S', 'M', 'L', or future sizes

@dataclass
class Event:
    id: int
    parcel_id: int
    event_type: str  # e.g., 'Arrival', 'Departure', 'PickedUp'
    event_time: datetime
    location: str

@dataclass
class User:
    id: int
    name: str
    email: str
    registered_date: datetime
