def baseline_detect(event):

    event_name = event.get(
        "eventName",
        ""
    )


    alerts = []


    if event_name == "AttachUserPolicy":

        alerts.append(
            {
                "scenario_id": event["scenario_id"],
                "alert_type": "IAM Privilege Escalation"
            }
        )


    elif event_name == "AttachRolePolicy":

        alerts.append(
            {
                "scenario_id": event["scenario_id"],
                "alert_type": "Role Abuse"
            }
        )


    elif event_name == "CreateAccessKey":

        alerts.append(
            {
                "scenario_id": event["scenario_id"],
                "alert_type": "Credential Escalation"
            }
        )


    elif event_name in [

        "StopLogging",

        "DeleteTrail"

    ]:

        alerts.append(
            {
                "scenario_id": event["scenario_id"],
                "alert_type": "CloudTrail Tampering"
            }
        )


    elif event_name == "AssumeRole":

        alerts.append(
            {
                "scenario_id": event["scenario_id"],
                "alert_type": "Role Abuse"
            }
        )


    return alerts