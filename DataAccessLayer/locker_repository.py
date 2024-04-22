from base_repository import BaseRepository

class LockerRepository(BaseRepository):
    def add_locker(self, locker):
        query = "INSERT INTO lockers (id, location, slots, slot_size) VALUES (?, ?, ?, ?)"
        params = (locker.id, locker.location, locker.slots, locker.slot_size)
        self._execute(query, params)

    def get_locker(self, locker_id):
        query = "SELECT * FROM lockers WHERE id = ?"
        params = (locker_id,)
        cursor = self._execute(query, params)
        return cursor.fetchone()
