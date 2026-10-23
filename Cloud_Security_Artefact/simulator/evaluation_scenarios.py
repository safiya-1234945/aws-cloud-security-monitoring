from datetime import datetime

from collector.event_receiver import receive_event

from config import EVALUATION_DATABASE



def send_event(
    event_name,
    username,
    source,
    policy=None
):


    event = {

        "eventTime":
        datetime.utcnow().isoformat(),

        "eventName":
        event_name,


        "eventSource":
        source,


        "username":
        username,


        "sourceIPAddress":
        "10.0.0.50"

    }


    if policy:

        event["policyArn"] = policy



    return receive_event(

        event,

        EVALUATION_DATABASE

    )





def scenario_privilege_escalation():


    print(
        "Scenario: IAM Privilege Escalation"
    )


    send_event(

        "CreateUser",

        "attacker-user",

        "iam.amazonaws.com"

    )


    send_event(

        "AttachUserPolicy",

        "attacker-user",

        "iam.amazonaws.com",

        "arn:aws:iam::aws:policy/AdministratorAccess"

    )


    send_event(

        "CreateAccessKey",

        "attacker-user",

        "iam.amazonaws.com"

    )





def scenario_credential_abuse():


    print(
        "Scenario: Credential Escalation"
    )


    send_event(

        "CreateAccessKey",

        "credential-user",

        "iam.amazonaws.com"

    )


    send_event(

        "ConsoleLogin",

        "credential-user",

        "signin.amazonaws.com"

    )





def scenario_cloudtrail_tampering():


    print(
        "Scenario: CloudTrail Tampering"
    )


    send_event(

        "StopLogging",

        "tamper-user",

        "cloudtrail.amazonaws.com"

    )


    send_event(

        "DeleteTrail",

        "tamper-user",

        "cloudtrail.amazonaws.com"

    )





def scenario_role_abuse():


    print(
        "Scenario: Role Abuse"
    )


    send_event(

        "AssumeRole",

        "role-user",

        "sts.amazonaws.com"

    )


    send_event(

        "AttachRolePolicy",

        "role-user",

        "iam.amazonaws.com",

        "arn:aws:iam::aws:policy/AdministratorAccess"

    )





def scenario_normal_activity():


    print(
        "Scenario: Normal Activity"
    )


    send_event(

        "ConsoleLogin",

        "normal-user",

        "signin.amazonaws.com"

    )


    send_event(

        "ListBuckets",

        "normal-user",

        "s3.amazonaws.com"

    )


    send_event(

        "GetObject",

        "normal-user",

        "s3.amazonaws.com"

    )





def main():


    print(

        "Running Controlled Evaluation Scenarios"

    )


    scenario_privilege_escalation()

    scenario_credential_abuse()

    scenario_role_abuse()

    scenario_cloudtrail_tampering()

    scenario_normal_activity()



    print(

        "Controlled Evaluation Scenarios Completed"

    )





if __name__ == "__main__":

    main()