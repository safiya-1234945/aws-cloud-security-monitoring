import pandas as pd


def extract_features(event):


    features = {}


    event_name = event.get(
        "eventName",
        ""
    )


    policy = event.get(
        "policyArn",
        ""
    )


    features["event_name"] = event_name


    features["username"] = event.get(
        "username",
        "unknown"
    )


    features["source_ip"] = event.get(
        "sourceIPAddress",
        "unknown"
    )


    features["timestamp"] = event.get(
        "eventTime",
        ""
    )


    features["iam_event"] = (
        1
        if "iam.amazonaws.com"
        in event.get(
            "eventSource",
            ""
        )
        else 0
    )


    features["privilege_change"] = (
        1
        if event_name in
        [
            "AttachUserPolicy",
            "AttachRolePolicy",
            "PutUserPolicy",
            "PutRolePolicy"
        ]
        else 0
    )


    features["administrator_policy"] = (
        1
        if "AdministratorAccess"
        in policy
        else 0
    )


    features["credential_creation"] = (
        1
        if event_name ==
        "CreateAccessKey"
        else 0
    )


    features["identity_creation"] = (
        1
        if event_name in
        [
            "CreateUser",
            "CreateRole"
        ]
        else 0
    )


    features["role_activity"] = (
        1
        if event_name in
        [
            "AssumeRole",
            "AttachRolePolicy"
        ]
        else 0
    )


    features["monitoring_change"] = (
        1
        if event_name in
        [
            "StopLogging",
            "DeleteTrail",
            "UpdateTrail"
        ]
        else 0
    )


    features["login_activity"] = (
        1
        if event_name ==
        "ConsoleLogin"
        else 0
    )


    return features



def create_feature_dataframe(events):


    feature_list = []


    for event in events:

        feature_list.append(
            extract_features(event)
        )


    return pd.DataFrame(
        feature_list
    )