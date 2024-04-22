from base_repository import BaseRepository

class EventRepository(BaseRepository):
    def add_event(self, event):
        query = "INSERT INTO events (id, parcel_id, event_type, event_time, location) VALUES (?, ?, ?, ?, ?)"
        params = (event.id, event.parcel_id, event.event_type, event.event_time, event.location)
        self._execute(query, params)

    def get_events_by_parcel(self, parcel_id):
        query = "SELECT * FROM events WHERE parcel_id = ?"
        params = (parcel_id,)
        cursor = self._execute(query, params)
        return cursor.fetchall()
