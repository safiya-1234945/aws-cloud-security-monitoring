# AWS Cloud Security Monitoring Prototype

## Overview

This project implements an AWS-focused cloud security monitoring prototype designed to identify selected suspicious identity and account-management activities from CloudTrail-style event records. It combines event ingestion, feature extraction, rule-based detection, time-bounded attack-chain correlation, SQLite storage and a Streamlit dashboard.

The artefact focuses on identifying potentially suspicious activity involving AWS Identity and Access Management (IAM), credential creation, role usage and CloudTrail monitoring changes. It also includes a controlled evaluation framework for comparing the proposed correlation approach against a static baseline.

**Project type:** MSc cybersecurity project and proof of concept  
**Platform focus:** Amazon Web Services (AWS)  
**Implementation:** Python, SQLite, Streamlit and pandas  
**Evaluation approach:** Simulated events and controlled test scenarios

This is a prototype for academic evaluation, not a production-ready security monitoring service.

## Objectives

The project aims to:

- Process CloudTrail-style event records through a structured monitoring pipeline.
- Extract security-relevant features from event data.
- Detect selected suspicious IAM, credential, role and monitoring activities.
- Correlate related events into configured attack sequences within a five-minute time window.
- Store events and generated alerts in SQLite databases.
- Present alerts, event information and investigation evidence through an interactive dashboard.
- Evaluate detection performance, event visibility and time-to-detection against controlled scenarios.

## Architecture

The processing workflow follows this sequence:

1. **Event collection:** The event receiver accepts an event, initialises the relevant database, stores the event and passes it to the processing pipeline.
2. **Feature engineering:** Event fields are transformed into security indicators, including identity, source IP, timestamp, IAM activity, privilege changes, credential creation, role activity and monitoring changes.
3. **Rule-based detection:** Detection rules identify selected suspicious activities and assign alert categories, severity, confidence and explanatory reasons.
4. **Attack-chain correlation:** The correlation engine checks configured event sequences associated with selected attack scenarios.
5. **Evidence generation:** Supporting event details and detection explanations are attached to alerts.
6. **Database storage:** SQLite stores event and alert records for subsequent analysis and dashboard display.
7. **Dashboard and evaluation:** Streamlit presents monitoring information, while evaluation scripts calculate detection metrics and generate analytical outputs.

## Detection Coverage

The prototype contains rules and correlation logic for the following categories.

| Category | Configured event sequence or indicator |
|---|---|
| IAM privilege escalation | `CreateUser` → `AttachUserPolicy` → `CreateAccessKey` |
| Role abuse | `AssumeRole` → `AttachRolePolicy` |
| CloudTrail tampering | `StopLogging` → `DeleteTrail` |
| Credential escalation | Detection of `CreateAccessKey` activity |

The correlation engine uses a **300-second (five-minute) time window** for its configured attack chains. Individual event-level rules also detect selected indicators, such as administrator-level IAM policy assignment and cloud credential creation.

These rules cover selected scenarios rather than every possible AWS attack technique. Detection results depend on the available event fields, configured rules and event sequences.

## Project Structure

```text
Cloud_Security_Artefact/
├── collector/
│   └── event_receiver.py
├── dashboard/
│   └── app.py
├── database/
│   └── database.py
├── detection/
│   ├── detection_engine.py
│   ├── correlation_engine.py
│   ├── evidence_generator.py
│   ├── test_detection.py
│   └── test_correlation.py
├── evaluation/
│   ├── baseline_engine.py
│   ├── evaluator.py
│   ├── framework_runner.py
│   ├── scenario_generator.py
│   ├── run_comparison.py
│   ├── run_large_scale.py
│   ├── log_visibility.py
│   ├── time_to_detection.py
│   └── generate_evaluation_graphs.py
├── processing/
│   ├── feature_engineering.py
│   └── stream_processor.py
├── config.py
├── requirements.txt
└── README.md
```

The repository may contain additional files and subfolders, including model, simulator, risk and evaluation-result components. The structure above highlights the principal modules rather than listing every file.

## Requirements

- Python 3.10 or a compatible version supported by the installed dependencies
- pip
- The packages specified in `requirements.txt`

The dashboard uses Streamlit, SQLite and pandas. Evaluation graph generation uses pandas and Matplotlib.

## Installation

Clone the repository:

```bash
git clone https://github.com/safiya-1234945/aws-cloud-security-monitoring.git
cd aws-cloud-security-monitoring
```

Create and activate a virtual environment.

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Run commands from the repository root so that Python package imports and configured paths resolve correctly.

## Running the Dashboard

Launch the Streamlit application:

```bash
python -m streamlit run dashboard/app.py
```

The dashboard displays available event and alert records, summary metrics, alert distributions, severity and attack-type filters, investigation details, supporting evidence and recent cloud events.

The dashboard reads from the production database configured in `config.py`. If no existing records are available, the dashboard may initially show empty results until events have been processed.

## Running the Evaluation

The evaluation modules generate controlled scenarios and compare the static baseline with the proposed correlation framework.

Run the comparison evaluation:

```bash
python -m evaluation.run_comparison
```

Run the larger scenario evaluation:

```bash
python -m evaluation.run_large_scale
```

Calculate log visibility coverage:

```bash
python -m evaluation.log_visibility
```

Calculate time-to-detection results:

```bash
python -m evaluation.time_to_detection
```

Generate evaluation graphs:

```bash
python -m evaluation.generate_evaluation_graphs
```

The graph-generation script expects the relevant evaluation result CSV files in the configured results directory. Run the necessary evaluation scripts first and check that their expected output files exist before generating the graphs.

**Database caution:** The evaluation scripts can reset or delete the configured evaluation database before running an experiment. Back up any evaluation records you need to retain before executing them.

## Evaluation Method

The framework is assessed using controlled scenarios containing labelled attack and benign activity. The evaluation code calculates:

- True positives
- False positives
- False negatives
- Precision
- Recall
- F1 score

Additional scripts examine visibility of the event types required by the configured attack chains and calculate time-to-detection from stored event and alert timestamps.

Results should be interpreted within the limits of the experimental setup. Simulated scenarios do not establish detection effectiveness under all real-world AWS conditions, and measured prototype processing times should not be interpreted as end-to-end production alert latency.

## Databases and Configuration

Database paths are defined in `config.py`:

- `production.db` — used by the dashboard and the production event-processing configuration.
- `evaluation.db` — used by the controlled evaluation workflow.

The database module initialises the `events` and `alerts` tables when required. Keep the configuration and database directory structure consistent with the code.

Do not publish AWS credentials, access keys, passwords, tokens or sensitive operational records. If a database contains sensitive information, replace it with a sanitised demonstration copy before making the repository public.

## Limitations

- The project is a proof of concept and has not been established as a continuously operating production service.
- Evaluation uses simulated CloudTrail-style events and controlled scenarios.
- Detection is limited to the implemented rules and configured correlation chains.
- The results do not establish comprehensive coverage of all AWS threats.
- Automated containment and remediation are not demonstrated.

## Academic Use

This repository supports the accompanying MSc cybersecurity project and its evaluation of a rule-based, correlation-oriented AWS cloud security monitoring prototype. It is provided for academic review, reproducibility and further development.

**Repository:** https://github.com/safiya-1234945/aws-cloud-security-monitoring
