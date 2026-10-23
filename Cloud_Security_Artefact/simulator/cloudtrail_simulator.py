import time
import random
from datetime import datetime, timezone

from collector.event_receiver import receive_event

from config import PRODUCTION_DATABASE



users = [
    "admin-user",
    "developer-user",
    "test-user",
    "unknown-user"
]


normal_events = [

    {
        "eventName": "ConsoleLogin",
        "eventSource": "signin.amazonaws.com"
    },

    {
        "eventName": "ListBuckets",
        "eventSource": "s3.amazonaws.com"
    },

    {
        "eventName": "GetObject",
        "eventSource": "s3.amazonaws.com"
    }

]


attack_events = [

    {
        "eventName": "CreateUser",
        "eventSource": "iam.amazonaws.com"
    },

    {
        "eventName": "AttachUserPolicy",
        "eventSource": "iam.amazonaws.com",
        "policyArn":
        "arn:aws:iam::aws:policy/AdministratorAccess"
    },

    {
        "eventName": "CreateAccessKey",
        "eventSource": "iam.amazonaws.com"
    },

    {
        "eventName": "StopLogging",
        "eventSource": "cloudtrail.amazonaws.com"
    }

]



def generate_event():


    if random.random() < 0.25:

        event = random.choice(
            attack_events
        )

    else:

        event = random.choice(
            normal_events
        )


    cloudtrail_event = {


        "eventTime":
        datetime.now(
            timezone.utc
        ).isoformat(),


        "eventName":
        event["eventName"],


        "eventSource":
        event["eventSource"],


        "username":
        random.choice(users),


        "sourceIPAddress":
        f"192.168.1.{random.randint(1,250)}"

    }



    if "policyArn" in event:

        cloudtrail_event[
            "policyArn"
        ] = event[
            "policyArn"
        ]


    return cloudtrail_event





def start_simulation():


    print(
        "Live CloudTrail Simulator Started"
    )


    while True:


        event = generate_event()


        print(
            event
        )


        receive_event(
            event,
            PRODUCTION_DATABASE
        )


        time.sleep(2)





if __name__ == "__main__":

    start_simulation()