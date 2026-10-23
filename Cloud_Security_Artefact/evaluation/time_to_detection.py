import sqlite3
import pandas as pd

from config import EVALUATION_DATABASE



ATTACK_EVENTS = {


    "IAM Privilege Escalation":

    [

        "CreateUser",

        "AttachUserPolicy",

        "CreateAccessKey"

    ],


    "Role Abuse":

    [

        "AssumeRole",

        "AttachRolePolicy"

    ],


    "CloudTrail Tampering":

    [

        "StopLogging",

        "DeleteTrail"

    ],


    "Credential Escalation":

    [

        "CreateAccessKey"

    ]

}



def calculate_ttd():


    conn = sqlite3.connect(

        EVALUATION_DATABASE

    )


    events = pd.read_sql_query(

        """

        SELECT *

        FROM events

        """,

        conn

    )


    alerts = pd.read_sql_query(

        """

        SELECT *

        FROM alerts

        """,

        conn

    )


    conn.close()



    events["timestamp"] = pd.to_datetime(

        events["timestamp"],

        format="ISO8601"

    )


    alerts["timestamp"] = pd.to_datetime(

        alerts["timestamp"],

        format="ISO8601"

    )



    results = []



    for _, alert in alerts.iterrows():


        username = alert["username"]


        attack_type = alert["alert_type"]



        user_events = events[

            events["username"]

            ==

            username

        ].copy()



        if user_events.empty:

            continue



        user_events = user_events.sort_values(

            "timestamp"

        )



        if attack_type not in ATTACK_EVENTS:

            continue



        required_events = ATTACK_EVENTS[

            attack_type

        ]



        attack_events = user_events[

            user_events["event_name"].isin(

                required_events

            )

        ]



        if attack_events.empty:

            continue



        first_event_time = attack_events[

            "timestamp"

        ].min()



        alert_time = alert["timestamp"]



        ttd_ms = (

            alert_time -

            first_event_time

        ).total_seconds() * 1000



        results.append(

            {

                "Attack Type":

                attack_type,


                "First Attack Event":

                attack_events.iloc[0]["event_name"],


                "Alert Event Time":

                alert_time,


                "TTD_milliseconds":

                round(

                    ttd_ms,

                    3

                )

            }

        )



    result = pd.DataFrame(

        results

    )



    if result.empty:

        print(

            "No detection records found"

        )

        return



    summary = result.groupby(

        "Attack Type"

    )["TTD_milliseconds"].mean().reset_index()



    print()

    print(

        "Time To Detection Results"

    )

    print(summary)



    print()

    print(

        "Overall Average TTD:",

        round(

            summary["TTD_milliseconds"].mean(),

            3

        ),

        "milliseconds"

    )



    summary.to_csv(

        "evaluation/results/time_to_detection.csv",

        index=False

    )


    print()

    print(

        "Saved: evaluation/results/time_to_detection.csv"

    )



if __name__ == "__main__":

    calculate_ttd()