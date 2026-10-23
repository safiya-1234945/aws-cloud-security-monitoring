def detect_privilege_escalation(features):

    findings = []


    if (
        features["privilege_change"] == 1
        and
        features["administrator_policy"] == 1
    ):

        findings.append({

            "alert_type":
            "IAM Privilege Escalation",

            "severity":
            "HIGH",

            "confidence":
            0.95,

            "reason":
            "Administrator-level IAM policy assigned",

            "username":
            features["username"],

            "timestamp":
            features["timestamp"]

        })


    return findings



def detect_credential_escalation(features):

    findings = []


    if features["credential_creation"] == 1:


        findings.append({

            "alert_type":
            "Credential Escalation",

            "severity":
            "HIGH",

            "confidence":
            0.85,

            "reason":
            "New cloud access credential created",

            "username":
            features["username"],

            "timestamp":
            features["timestamp"]

        })


    return findings



def detect_role_abuse(features):

    findings = []


    if features["role_activity"] == 1:


        findings.append({

            "alert_type":
            "Role Abuse",

            "severity":
            "HIGH",

            "confidence":
            0.90,

            "reason":
            "Cloud role permissions modified or assumed",

            "username":
            features["username"],

            "timestamp":
            features["timestamp"]

        })


    return findings



def detect_monitoring_tampering(features):

    findings = []


    if features["monitoring_change"] == 1:


        findings.append({

            "alert_type":
            "CloudTrail Tampering",

            "severity":
            "CRITICAL",

            "confidence":
            0.98,

            "reason":
            "Cloud monitoring configuration modified",

            "username":
            features["username"],

            "timestamp":
            features["timestamp"]

        })


    return findings




def analyse_event(features):


    alerts = []


    alerts.extend(
        detect_privilege_escalation(
            features
        )
    )


    alerts.extend(
        detect_credential_escalation(
            features
        )
    )


    alerts.extend(
        detect_role_abuse(
            features
        )
    )


    alerts.extend(
        detect_monitoring_tampering(
            features
        )
    )


    return alerts