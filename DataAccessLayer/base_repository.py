import sqlite3

class BaseRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _execute(self, query, params=None):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or [])
            return cursor

    def _execute_many(self, query, params_list):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            return cursor
