import sqlite3
import os

from config import PRODUCTION_DATABASE



def initialise_database(database_path):


    os.makedirs(
        "database",
        exist_ok=True
    )


    connection = sqlite3.connect(
        database_path
    )


    cursor = connection.cursor()


    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS events
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            event_name TEXT,
            username TEXT,
            source_ip TEXT,
            event_source TEXT,
            raw_event TEXT
        )
        """
    )


    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS alerts
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            username TEXT,
            alert_type TEXT,
            severity TEXT,
            confidence REAL,
            reason TEXT,
            evidence TEXT
        )
        """
    )


    connection.commit()

    connection.close()




def store_event(event, database_path):


    connection = sqlite3.connect(
        database_path
    )


    cursor = connection.cursor()


    cursor.execute(

        """
        INSERT INTO events
        (
        timestamp,
        event_name,
        username,
        source_ip,
        event_source,
        raw_event
        )

        VALUES (?, ?, ?, ?, ?, ?)

        """,

        (

        event.get("eventTime"),

        event.get("eventName"),

        event.get("username"),

        event.get("sourceIPAddress"),

        event.get("eventSource"),

        str(event)

        )

    )


    connection.commit()

    connection.close()




def store_alert(alert, database_path):


    connection = sqlite3.connect(
        database_path
    )


    cursor = connection.cursor()


    cursor.execute(

        """
        INSERT INTO alerts
        (
        timestamp,
        username,
        alert_type,
        severity,
        confidence,
        reason,
        evidence
        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

        """,

        (

        alert.get("timestamp"),

        alert.get("username"),

        alert.get("alert_type"),

        alert.get("severity"),

        alert.get("confidence"),

        alert.get("reason"),

        str(alert.get("evidence"))

        )

    )


    connection.commit()

    connection.close()