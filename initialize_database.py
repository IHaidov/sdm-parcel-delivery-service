import sqlite3

def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """ Create a table from the create_table_sql statement """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def main():
    database = "path_to_db.sqlite"

    sql_create_parcels_table = """ CREATE TABLE IF NOT EXISTS parcels (
                                        id integer PRIMARY KEY,
                                        sender_id integer NOT NULL,
                                        recipient_id integer NOT NULL,
                                        registered_time text NOT NULL,
                                        delivery_time text,
                                        pick_up_time text,
                                        size text NOT NULL
                                    ); """

    sql_create_lockers_table = """ CREATE TABLE IF NOT EXISTS lockers (
                                        id integer PRIMARY KEY,
                                        location text NOT NULL,
                                        slots integer NOT NULL,
                                        slot_size text NOT NULL
                                    ); """

    sql_create_events_table = """ CREATE TABLE IF NOT EXISTS events (
                                        id integer PRIMARY KEY,
                                        parcel_id integer NOT NULL,
                                        event_type text NOT NULL,
                                        event_time text NOT NULL,
                                        location text NOT NULL,
                                        FOREIGN KEY (parcel_id) REFERENCES parcels (id)
                                    ); """

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        email text NOT NULL,
                                        registered_date text NOT NULL
                                    ); """

    # Create a database connection
    conn = create_connection(database)

    # Create tables
    if conn is not None:
        create_table(conn, sql_create_parcels_table)
        create_table(conn, sql_create_lockers_table)
        create_table(conn, sql_create_events_table)
        create_table(conn, sql_create_users_table)
        conn.close()
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
