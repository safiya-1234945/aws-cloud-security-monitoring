import os
import pandas as pd
import matplotlib.pyplot as plt


from config import EVALUATION_DATABASE

from database.database import initialise_database

from evaluation.scenario_generator import generate_scenarios

from evaluation.baseline_engine import baseline_detect

from evaluation.framework_runner import run_framework

from evaluation.evaluator import calculate_metrics

from processing.stream_processor import reset_event_buffer



RESULT_FILE = (
    "evaluation/results/large_scale_results.csv"
)



def reset_database():

    if os.path.exists(
        EVALUATION_DATABASE
    ):

        os.remove(
            EVALUATION_DATABASE
        )



def run_experiment(size):


    reset_database()


    initialise_database(
        EVALUATION_DATABASE
    )


    reset_event_buffer()



    scenarios = generate_scenarios(
        size
    )



    baseline_alerts = []



    for scenario in scenarios:


        for event in scenario["events"]:


            baseline_alerts.extend(

                baseline_detect(
                    event
                )

            )



    framework_alerts = run_framework(

        scenarios

    )



    baseline_results = calculate_metrics(

        scenarios,

        baseline_alerts

    )


    framework_results = calculate_metrics(

        scenarios,

        framework_alerts

    )



    return [


        {

        "Scenario Size":
        size,

        "Framework":
        "Static Baseline",

        **baseline_results

        },


        {

        "Scenario Size":
        size,

        "Framework":
        "Proposed Correlation Framework",

        **framework_results

        }

    ]





def create_chart(results):


    df = pd.DataFrame(
        results
    )


    pivot = df.pivot(

        index="Scenario Size",

        columns="Framework",

        values="F1 Score"

    )


    pivot.plot(
        kind="bar"
    )


    plt.ylabel(
        "F1 Score"
    )


    plt.title(
        "Framework Performance Comparison"
    )


    plt.tight_layout()


    plt.savefig(

        "evaluation/results/comparison_chart.png"

    )



def main():


    print(
        "Large Scale Evaluation Started"
    )



    all_results = []



    for size in [

        100,

        500,

        1000

    ]:


        print(
            f"Running {size} scenarios"
        )


        results = run_experiment(
            size
        )


        all_results.extend(
            results
        )



    os.makedirs(

        "evaluation/results",

        exist_ok=True

    )



    df = pd.DataFrame(
        all_results
    )


    df.to_csv(

        RESULT_FILE,

        index=False

    )



    create_chart(
        all_results
    )



    print(
        "Large Scale Evaluation Completed"
    )


    print(df)




if __name__ == "__main__":

    main()