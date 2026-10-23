from collector.event_receiver import receive_event


events = [

{
"eventName":"AssumeRole",
"eventSource":"sts.amazonaws.com",
"username":"attacker-user",
"sourceIPAddress":"192.168.1.20"
},

{
"eventName":"AttachRolePolicy",
"eventSource":"iam.amazonaws.com",
"username":"attacker-user",
"sourceIPAddress":"192.168.1.20",
"policyArn":"arn:aws:iam::aws:policy/AdministratorAccess"
}

]


for event in events:

    print(
        receive_event(event)
    )