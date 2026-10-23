from detection_engine import analyse_event


features = {

    "username":
    "test-user",

    "timestamp":
    "2026-10-08T10:00:00",

    "privilege_change":
    1,

    "administrator_policy":
    1,

    "credential_creation":
    0,

    "monitoring_change":
    0

}


alerts = analyse_event(
    features
)


print(alerts)