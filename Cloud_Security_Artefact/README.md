Cloud Security Monitoring Artefact

Setup
Requires Python 3.10+ on Windows.
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install pandas matplotlib streamlit

Run the tests
python processing\test_features.py
python detection\test_detection.py
python detection\test_correlation.py
The tests check feature extraction, event-level detection, and
correlation of the CreateUser → AttachUserPolicy → CreateAccessKey
sequence.

Run the evaluation
python -m evaluation.run_comparison
python -m evaluation.run_large_scale
python -m simulator.evaluation_scenarios
python -m evaluation.log_visibility
python -m evaluation.time_to_detection
python -m evaluation.generate_evaluation_graphs
The evaluation compares the proposed correlation framework with the
static baseline and generates CSV results and graphs under
evaluation\results\. The visibility and time-to-detection scripts use
the evaluation database, so run the scenario generator immediately
before these two scripts if they should evaluate the controlled
scenarios.

Launch the dashboard
Run the simulator in one PowerShell window:
python -m simulator.cloudtrail_simulator
In a second PowerShell window, run:
streamlit run dashboard\app.py
Open the local URL printed by Streamlit (normally
http://localhost:8501). The simulator generates synthetic
CloudTrail-style events; it does not connect to a live AWS account.

Main outputs
- evaluation\results\comparison_report.csv --- baseline comparison
- evaluation\results\large_scale_results.csv --- results for 100,
  500 and 1,000 scenarios
- evaluation\results\log_visibility_coverage.csv --- required-event
  coverage
- evaluation\results\time_to_detection.csv --- local processing
  latency
- evaluation\results\*.png --- evaluation graphs