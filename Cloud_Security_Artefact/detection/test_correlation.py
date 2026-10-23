from correlation_engine import correlate_events



events = [


{
    "eventName":
    "CreateUser",

    "username":
    "attacker-user"
},


{
    "eventName":
    "AttachUserPolicy",

    "username":
    "attacker-user"
},


{
    "eventName":
    "CreateAccessKey",

    "username":
    "attacker-user"
}


]



result = correlate_events(
    events
)


print(result)