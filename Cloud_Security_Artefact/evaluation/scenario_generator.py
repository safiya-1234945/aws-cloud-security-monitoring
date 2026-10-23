import random
from datetime import datetime, timedelta


def create_event(
    scenario_id,
    event_name,
    username,
    source,
    timestamp
):

    return {

        "scenario_id": scenario_id,

        "eventTime": timestamp.isoformat(),

        "eventName": event_name,

        "eventSource": source,

        "username": username,

        "sourceIPAddress": "10.0.0.50"

    }



def generate_scenarios(
    total_scenarios=100
):


    scenarios = []

    scenario_id = 1



    attack_scenarios = [

        (
            "IAM Privilege Escalation",
            [
                ("CreateUser", "iam.amazonaws.com"),
                ("AttachUserPolicy", "iam.amazonaws.com"),
                ("CreateAccessKey", "iam.amazonaws.com")
            ],
            "YES"
        ),


        (
            "Credential Escalation",
            [
                ("CreateAccessKey", "iam.amazonaws.com"),
                ("ConsoleLogin", "signin.amazonaws.com")
            ],
            "YES"
        ),


        (
            "Role Abuse",
            [
                ("AssumeRole", "sts.amazonaws.com"),
                ("AttachRolePolicy", "iam.amazonaws.com")
            ],
            "YES"
        ),


        (
            "CloudTrail Tampering",
            [
                ("StopLogging", "cloudtrail.amazonaws.com"),
                ("DeleteTrail", "cloudtrail.amazonaws.com")
            ],
            "YES"
        )

    ]



    benign_scenarios = [

        (
            "Normal IAM Update",
            [
                ("AttachUserPolicy", "iam.amazonaws.com")
            ],
            "NO"
        ),


        (
            "Normal Credential Rotation",
            [
                ("CreateAccessKey", "iam.amazonaws.com")
            ],
            "NO"
        ),


        (
            "Normal Role Usage",
            [
                ("AssumeRole", "sts.amazonaws.com")
            ],
            "NO"
        ),


        (
            "Normal Monitoring Change",
            [
                ("StopLogging", "cloudtrail.amazonaws.com")
            ],
            "NO"
        )

    ]



    templates = (

        attack_scenarios +

        benign_scenarios

    )



    for i in range(total_scenarios):


        name, events, label = random.choice(
            templates
        )


        username = f"user-{i}"


        start_time = datetime.utcnow()


        event_list = []



        for position, (event, source) in enumerate(events):


            event_list.append(

                create_event(

                    scenario_id,

                    event,

                    username,

                    source,

                    start_time +

                    timedelta(

                        seconds=position * 30

                    )

                )

            )



        scenarios.append(

            {

                "scenario_id":

                scenario_id,


                "scenario_type":

                name,


                "expected_detection":

                label,


                "events":

                event_list

            }

        )


        scenario_id += 1



    return scenarios