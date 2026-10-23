from collector.event_receiver import receive_event



events = [


{
"eventName":
"CreateUser",

"eventSource":
"iam.amazonaws.com",

"username":
"attacker-user",

"sourceIPAddress":
"192.168.1.10"
},


{
"eventName":
"AttachUserPolicy",

"eventSource":
"iam.amazonaws.com",

"username":
"attacker-user",

"sourceIPAddress":
"192.168.1.10",

"policyArn":
"arn:aws:iam::aws:policy/AdministratorAccess"
},


{
"eventName":
"CreateAccessKey",

"eventSource":
"iam.amazonaws.com",

"username":
"attacker-user",

"sourceIPAddress":
"192.168.1.10"
}


]



for event in events:

    result = receive_event(
        event
    )

    print(result)