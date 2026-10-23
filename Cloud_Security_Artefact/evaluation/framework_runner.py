from collector.event_receiver import receive_event

from processing.stream_processor import reset_event_buffer

from config import EVALUATION_DATABASE



def run_framework(
    scenarios
):


    framework_alerts = []


    for scenario in scenarios:


        reset_event_buffer()


        scenario_id = scenario["scenario_id"]



        for event in scenario["events"]:


            result = receive_event(

                event,

                EVALUATION_DATABASE

            )


            for alert in result.get(

                "chain_alerts",

                []

            ):


                framework_alerts.append(

                    {

                    "scenario_id":
                    scenario_id,


                    "alert_type":
                    alert["alert_type"]

                    }

                )


    return framework_alerts