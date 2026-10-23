from database.database import (
    store_event,
    initialise_database
)


from processing.stream_processor import process_event



def receive_event(
    event,
    database_path
):


    initialise_database(
        database_path
    )


    store_event(
        event,
        database_path
    )


    result = process_event(
        event,
        database_path
    )


    return result