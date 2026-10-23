from processing.feature_engineering import extract_features

from detection.detection_engine import analyse_event

from detection.correlation_engine import correlate_events

from detection.evidence_generator import generate_evidence

from database.database import store_alert



event_buffer = []



def reset_event_buffer():

    global event_buffer

    event_buffer = []





def process_event(
    event,
    database_path
):


    event_buffer.append(
        event
    )


    features = extract_features(
        event
    )


    alerts = analyse_event(
        features
    )


    for alert in alerts:


        alert["evidence"] = generate_evidence(

            event,

            alert

        )


        store_alert(

            alert,

            database_path

        )



    chain_alerts = correlate_events(

        event_buffer

    )



    for alert in chain_alerts:


        alert["evidence"] = {

            "attack_chain":
            alert.get("events"),

            "username":
            alert.get("username"),

            "reason":
            alert.get("reason")

        }


        store_alert(

            alert,

            database_path

        )


    return {

        "features":
        features,

        "alerts":
        alerts,

        "chain_alerts":
        chain_alerts

    }