from feature_engineering import extract_features



event = {

    "eventName":
    "AttachUserPolicy",

    "eventSource":
    "iam.amazonaws.com",

    "username":
    "test-user",

    "sourceIPAddress":
    "192.168.1.50",

    "policyArn":
    "arn:aws:iam::aws:policy/AdministratorAccess"

}



features = extract_features(
    event
)


print(features)