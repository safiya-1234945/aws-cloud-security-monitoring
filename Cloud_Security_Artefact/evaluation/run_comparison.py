import os
import pandas as pd

from config import EVALUATION_DATABASE

from database.database import initialise_database

from evaluation.scenario_generator import generate_scenarios

from evaluation.baseline_engine import baseline_detect

from evaluation.framework_runner import run_framework

from evaluation.evaluator import calculate_metrics



def reset_database():

    if os.path.exists(
        EVALUATION_DATABASE
    ):

        os.remove(
            EVALUATION_DATABASE
        )



def main():

    print(
        "Evaluation Started"
    )


    reset_database()


    initialise_database(
        EVALUATION_DATABASE
    )


    scenarios = generate_scenarios()



    baseline_detections = []


    for scenario in scenarios:


        for event in scenario["events"]:


            baseline_detections.extend(

                baseline_detect(
                    event
                )

            )



    framework_detections = run_framework(
        scenarios
    )



    baseline_results = calculate_metrics(

        scenarios,

        baseline_detections

    )



    framework_results = calculate_metrics(

        scenarios,

        framework_detections

    )



    results = pd.DataFrame(

        [

            {

                "Framework":

                "Static Baseline",

                **baseline_results

            },


            {

                "Framework":

                "Proposed Correlation Framework",

                **framework_results

            }

        ]

    )



    os.makedirs(

        "evaluation/results",

        exist_ok=True

    )


    results.to_csv(

        "evaluation/results/comparison_report.csv",

        index=False

    )


    print()

    print(results)




if __name__ == "__main__":

    main()