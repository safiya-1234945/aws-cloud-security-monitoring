def generate_evidence(event, alert):


    evidence = {

        "username":
        event.get(
            "username",
            "unknown"
        ),

        "source_ip":
        event.get(
            "sourceIPAddress",
            "unknown"
        ),

        "event":
        event.get(
            "eventName",
            "unknown"
        ),

        "event_source":
        event.get(
            "eventSource",
            "unknown"
        )

    }


    if "policyArn" in event:

        evidence[
            "policy"
        ] = event[
            "policyArn"
        ]


    evidence[
        "detection_reason"
    ] = alert.get(
        "reason"
    )


    return evidence