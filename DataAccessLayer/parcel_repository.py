from DataAccessLayer.base_repository import BaseRepository

class ParcelRepository(BaseRepository):
    def add_parcel(self, parcel):
        query = "INSERT INTO parcels (id, sender_id, recipient_id, registered_time, delivery_time, pick_up_time, size) VALUES (?, ?, ?, ?, ?, ?, ?)"
        params = (parcel.id, parcel.sender_id, parcel.recipient_id, parcel.registered_time, parcel.delivery_time, parcel.pick_up_time, parcel.size)
        self._execute(query, params)

    def get_parcel(self, parcel_id):
        query = "SELECT * FROM parcels WHERE id = ?"
        params = (parcel_id,)
        cursor = self._execute(query, params)
        return cursor.fetchone()

    def update_parcel(self, parcel):
        query = "UPDATE parcels SET delivery_time = ?, pick_up_time = ? WHERE id = ?"
        params = (parcel.delivery_time, parcel.pick_up_time, parcel.id)
        self._execute(query, params)

    def delete_parcel(self, parcel_id):
        query = "DELETE FROM parcels WHERE id = ?"
        params = (parcel_id,)
        self._execute(query, params)
