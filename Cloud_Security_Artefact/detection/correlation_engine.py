from datetime import datetime


ATTACK_CHAINS = {

    "IAM Privilege Escalation":

    [
        "CreateUser",
        "AttachUserPolicy",
        "CreateAccessKey"
    ],


    "CloudTrail Tampering":

    [
        "StopLogging",
        "DeleteTrail"
    ],


    "Role Abuse":

    [
        "AssumeRole",
        "AttachRolePolicy"
    ]

}



TIME_WINDOW_SECONDS = 300



def get_event_time(event):

    return (

        event.get("timestamp")

        or

        event.get("eventTime")

        or

        ""

    )



def get_event_name(event):

    return (

        event.get("event_name")

        or

        event.get("eventName")

        or

        ""

    )



def check_chain(events, chain):


    matched_events = []

    index = 0



    for event in events:


        if get_event_name(event) == chain[index]:


            matched_events.append(event)

            index += 1


            if index == len(chain):

                break



    if index != len(chain):

        return None



    first_time = datetime.fromisoformat(

        get_event_time(

            matched_events[0]

        )

    )


    last_time = datetime.fromisoformat(

        get_event_time(

            matched_events[-1]

        )

    )


    difference = (

        last_time -

        first_time

    ).total_seconds()



    if difference <= TIME_WINDOW_SECONDS:

        return matched_events



    return None





def correlate_events(events):


    alerts = []


    users = {}



    for event in events:


        username = event.get(

            "username",

            "unknown"

        )


        users.setdefault(

            username,

            []

        ).append(event)



    for username, user_events in users.items():


        user_events.sort(

            key=get_event_time

        )


        for attack, chain in ATTACK_CHAINS.items():


            matched = check_chain(

                user_events,

                chain

            )



            if matched:


                alerts.append(

                    {

                    "alert_type":

                    attack,


                    "username":

                    username,


                    "severity":

                    "CRITICAL",


                    "confidence":

                    0.98,


                    "reason":

                    "Ordered attack chain detected within time window",


                    "events":

                    chain,


                    "timestamp":

                    get_event_time(

                        matched[-1]

                    )

                    }

                )



    return alerts