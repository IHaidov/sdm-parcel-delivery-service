from DataAccessLayer.event_repository import EventRepository

class EventService:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def log_event(self, event):
        self.event_repository.add_event(event)

    def get_events_for_parcel(self, parcel_id):
        return self.event_repository.get_events_by_parcel(parcel_id)
