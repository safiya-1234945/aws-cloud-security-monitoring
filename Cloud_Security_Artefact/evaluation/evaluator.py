def calculate_metrics(
    scenarios,
    detections
):


    tp = 0

    fp = 0

    fn = 0



    scenario_map = {}


    for scenario in scenarios:

        scenario_map[
            scenario["scenario_id"]
        ] = scenario



    detected_scenarios = {}



    for detection in detections:


        scenario_id = detection["scenario_id"]


        detected_scenarios.setdefault(

            scenario_id,

            []

        ).append(

            detection["alert_type"]

        )



    for scenario in scenarios:


        scenario_id = scenario[
            "scenario_id"
        ]


        expected = scenario[
            "expected_detection"
        ]


        detected = detected_scenarios.get(

            scenario_id,

            []

        )



        if expected == "YES":


            if len(detected) > 0:

                tp += 1

            else:

                fn += 1



        else:


            if len(detected) > 0:

                fp += 1



    precision = (

        tp /

        (
            tp +
            fp
        )

    ) * 100 if (

        tp +
        fp

    ) else 0



    recall = (

        tp /

        (
            tp +
            fn
        )

    ) * 100 if (

        tp +
        fn

    ) else 0



    f1 = (

        2 *
        precision *
        recall /

        (
            precision +
            recall
        )

    ) if (

        precision +
        recall

    ) else 0



    return {


        "True Positive":
        tp,


        "False Positive":
        fp,


        "False Negative":
        fn,


        "Precision":
        round(
            precision,
            2
        ),


        "Recall":
        round(
            recall,
            2
        ),


        "F1 Score":
        round(
            f1,
            2
        )

    }