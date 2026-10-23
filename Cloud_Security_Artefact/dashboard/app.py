import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import streamlit as st
import sqlite3
import pandas as pd
import ast
import time


from config import PRODUCTION_DATABASE
from database.database import initialise_database



st.set_page_config(
    page_title="Cloud Security Monitoring Dashboard",
    layout="wide"
)



initialise_database(
    PRODUCTION_DATABASE
)



def load_events():

    conn = sqlite3.connect(
        PRODUCTION_DATABASE
    )

    df = pd.read_sql_query(
        """
        SELECT *
        FROM events
        ORDER BY id DESC
        LIMIT 100
        """,
        conn
    )

    conn.close()

    return df



def load_alerts():

    conn = sqlite3.connect(
        PRODUCTION_DATABASE
    )

    df = pd.read_sql_query(
        """
        SELECT *
        FROM alerts
        ORDER BY id DESC
        LIMIT 100
        """,
        conn
    )

    conn.close()

    return df



events = load_events()

alerts = load_alerts()



st.title(
    "Real-Time Cloud Security Monitoring Dashboard"
)



if len(alerts) > 0:


    col1, col2, col3, col4 = st.columns(4)


    with col1:
        st.metric(
            "Events Processed",
            len(events)
        )


    with col2:
        st.metric(
            "Active Alerts",
            len(alerts)
        )


    with col3:

        critical = len(
            alerts[
                alerts["severity"] == "CRITICAL"
            ]
        )

        st.metric(
            "Critical Incidents",
            critical
        )


    with col4:

        attack_count = alerts[
            "alert_type"
        ].nunique()

        st.metric(
            "Attack Categories",
            attack_count
        )



st.divider()



st.sidebar.header(
    "Alert Filters"
)



if len(alerts) > 0:


    severity_filter = st.sidebar.multiselect(

        "Severity",

        alerts["severity"].unique(),

        default=list(
            alerts["severity"].unique()
        )

    )


    attack_filter = st.sidebar.multiselect(

        "Attack Type",

        alerts["alert_type"].unique(),

        default=list(
            alerts["alert_type"].unique()
        )

    )


    filtered_alerts = alerts[

        (alerts["severity"].isin(severity_filter))
        &
        (alerts["alert_type"].isin(attack_filter))

    ]

else:

    filtered_alerts = alerts



st.subheader(
    "Security Analytics"
)



if len(alerts) > 0:


    col1, col2 = st.columns(2)


    with col1:

        st.write(
            "Alerts by Attack Type"
        )

        attack_chart = (

            alerts[
                "alert_type"
            ]
            .value_counts()

        )


        st.bar_chart(
            attack_chart
        )



    with col2:

        st.write(
            "Severity Distribution"
        )

        severity_chart = (

            alerts[
                "severity"
            ]
            .value_counts()

        )


        st.bar_chart(
            severity_chart
        )



st.divider()



st.subheader(
    "Latest Security Alerts"
)



if len(filtered_alerts) == 0:

    st.success(
        "No suspicious activity detected"
    )

else:


    st.dataframe(

        filtered_alerts[

            [
                "timestamp",
                "username",
                "alert_type",
                "severity",
                "confidence",
                "reason"
            ]

        ],

        use_container_width=True

    )



st.divider()



st.subheader(
    "Incident Investigation"
)



if len(filtered_alerts) > 0:


    selected = st.selectbox(

        "Select Alert",

        filtered_alerts.index

    )


    incident = filtered_alerts.loc[
        selected
    ]



    col1, col2 = st.columns(2)



    with col1:


        st.write(
            "### Alert Type"
        )

        st.write(
            incident["alert_type"]
        )


        st.write(
            "### User"
        )

        st.write(
            incident["username"]
        )


        st.write(
            "### Severity"
        )

        st.write(
            incident["severity"]
        )



    with col2:


        st.write(
            "### Confidence"
        )

        st.write(
            incident["confidence"]
        )


        st.write(
            "### Detection Reason"
        )

        st.write(
            incident["reason"]
        )



    st.write(
        "### Evidence"
    )


    try:


        evidence = ast.literal_eval(

            incident["evidence"]

        )


        st.json(
            evidence
        )



        if "attack_chain" in evidence:


            st.write(
                "### Attack Chain"
            )


            chain = evidence[
                "attack_chain"
            ]


            chain_text = ""


            for event in chain:

                chain_text += event + "\n\n↓\n\n"


            st.info(
                chain_text[:-7]
            )


    except:


        st.write(
            incident["evidence"]
        )



    st.write(
        "### Detection Explanation"
    )


    st.write(

        f"""
        **Trigger Event:**  
        {incident['alert_type']}


        **Logic Applied:**  
        The detection engine analysed CloudTrail activity,
        extracted security features, and matched the event
        against privilege escalation or malicious behaviour patterns.


        **Risk Indicator:**  
        {incident['reason']}


        **Evidence Source:**  
        User identity, source IP, event type and timestamp.
        """

    )



st.divider()



st.subheader(
    "Recent Cloud Events"
)



if len(events) > 0:


    st.dataframe(

        events[

            [
                "timestamp",
                "event_name",
                "username",
                "source_ip",
                "event_source"
            ]

        ],

        use_container_width=True

    )



time.sleep(5)

st.rerun()