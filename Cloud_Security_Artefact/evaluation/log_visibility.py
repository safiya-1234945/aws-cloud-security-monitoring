import sqlite3
import pandas as pd

from config import EVALUATION_DATABASE



ATTACK_CHAINS = {


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

    ]

}



def calculate_visibility():


    conn = sqlite3.connect(

        EVALUATION_DATABASE

    )


    events = pd.read_sql_query(

        """

        SELECT event_name

        FROM events

        """,

        conn

    )


    conn.close()



    captured_events = set(

        events["event_name"]

    )



    results = []



    total_required = 0

    total_captured = 0



    for attack, required_events in ATTACK_CHAINS.items():


        captured = 0



        for event in required_events:


            total_required += 1



            if event in captured_events:


                captured += 1

                total_captured += 1



        coverage = (

            captured /

            len(required_events)

        ) * 100



        results.append(

            {

                "Attack Chain":

                attack,


                "Required Events":

                len(required_events),


                "Captured Events":

                captured,


                "Coverage (%)":

                round(

                    coverage,

                    2

                )

            }

        )



    result = pd.DataFrame(

        results

    )



    overall = (

        total_captured /

        total_required

    ) * 100



    print()

    print(

        "Log Visibility Coverage Results"

    )

    print()

    print(result)



    print()

    print(

        "Overall Log Visibility Coverage:",

        round(

            overall,

            2

        ),

        "%"

    )



    result.to_csv(

        "evaluation/results/log_visibility_coverage.csv",

        index=False

    )


    print()

    print(

        "Saved: evaluation/results/log_visibility_coverage.csv"

    )



if __name__ == "__main__":

    calculate_visibility()