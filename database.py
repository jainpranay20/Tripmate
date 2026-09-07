import sqlite3


DATABASE_NAME = "tripmate.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def setup_database():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            destination TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'confirmed'
        )
        """
    )

    connection.commit()
    connection.close()


def create_trip(
    user_id: str,
    destination: str,
    start_date: str,
    end_date: str,
) -> int:

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO trips
        (
            user_id,
            destination,
            start_date,
            end_date
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            destination,
            start_date,
            end_date,
        ),
    )

    trip_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return trip_id


def get_trips(user_id: str):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            destination,
            start_date,
            end_date,
            status
        FROM trips
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,),
    )

    trips = cursor.fetchall()

    connection.close()

    return trips
