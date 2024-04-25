from datetime import datetime


class Event:
    def __init__(self, timestamp: datetime, location: str, event_type: str):
        self.timestamp = timestamp
        self.location = location
        self.type = event_type
