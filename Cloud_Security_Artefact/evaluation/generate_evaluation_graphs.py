
from pathlib import Path
import sys

import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent if SCRIPT_DIR.name.lower() == "evaluation" else SCRIPT_DIR
RESULT_DIR = SCRIPT_DIR / "results" if SCRIPT_DIR.name.lower() == "evaluation" else PROJECT_DIR / "evaluation" / "results"


def load_results(filename, required_columns=None):
    path = RESULT_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"Results file not found: {path}")

    df = pd.read_csv(path)

    if df.empty:
        raise ValueError(f"Results file is empty: {path}")

    if required_columns:
        missing = set(required_columns) - set(df.columns)
        if missing:
            raise ValueError(
                f"{filename} is missing columns: {', '.join(sorted(missing))}"
            )

    return df


def save_chart(filename):
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(RESULT_DIR / filename, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Created: {filename}")


def generate_performance_chart(df):
    metrics = ["Precision", "Recall", "F1 Score"]
    frameworks = list(df["Framework"].unique())
    scenario_sizes = sorted(df["Scenario Size"].unique())

    fig, axes = plt.subplots(
        1, len(scenario_sizes),
        figsize=(6 * len(scenario_sizes), 5),
        squeeze=False
    )
    axes = axes[0]

    x = list(range(len(metrics)))
    width = 0.8 / len(frameworks)

    for ax, size in zip(axes, scenario_sizes):
        subset = df[df["Scenario Size"] == size]

        for i, framework in enumerate(frameworks):
            row = subset[subset["Framework"] == framework]
            values = [row[metric].iloc[0] for metric in metrics]

            offsets = [
                position + (i - (len(frameworks) - 1) / 2) * width
                for position in x
            ]

            bars = ax.bar(
                offsets,
                values,
                width,
                label=framework
            )

            ax.bar_label(bars, fmt="%.1f", fontsize=8, padding=2)

        ax.set_title(f"{size} Scenarios")
        ax.set_xticks(x)
        ax.set_xticklabels(metrics)
        ax.set_ylabel("Score (%)")
        ax.set_ylim(0, 110)
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        ax.set_axisbelow(True)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=len(frameworks))
    fig.suptitle("Overall Detection Performance", y=1.04)
    fig.tight_layout()
    save_chart("overall_detection_performance.png")


def generate_detection_outcomes_chart(df):
    metrics = ["True Positive", "False Positive", "False Negative"]
    frameworks = list(df["Framework"].unique())
    scenario_sizes = sorted(df["Scenario Size"].unique())

    fig, axes = plt.subplots(
        1, len(scenario_sizes),
        figsize=(6 * len(scenario_sizes), 5),
        squeeze=False
    )
    axes = axes[0]

    x = list(range(len(metrics)))
    width = 0.8 / len(frameworks)

    for ax, size in zip(axes, scenario_sizes):
        subset = df[df["Scenario Size"] == size]

        for i, framework in enumerate(frameworks):
            row = subset[subset["Framework"] == framework]
            values = [row[metric].iloc[0] for metric in metrics]

            offsets = [
                position + (i - (len(frameworks) - 1) / 2) * width
                for position in x
            ]

            bars = ax.bar(
                offsets,
                values,
                width,
                label=framework
            )

            ax.bar_label(bars, fmt="%.0f", fontsize=8, padding=2)

        ax.set_title(f"{size} Scenarios")
        ax.set_xticks(x)
        ax.set_xticklabels(metrics, rotation=15, ha="right")
        ax.set_ylabel("Number of Scenarios")
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        ax.set_axisbelow(True)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=len(frameworks))
    fig.suptitle("Detection Outcomes Comparison", y=1.04)
    fig.tight_layout()
    save_chart("detection_outcomes_comparison.png")


def generate_performance_trends_chart(df):
    metrics = ["F1 Score", "Recall"]
    frameworks = list(df["Framework"].unique())

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for ax, metric in zip(axes, metrics):
        for framework in frameworks:
            group = df[df["Framework"] == framework].sort_values("Scenario Size")

            ax.plot(
                group["Scenario Size"],
                group[metric],
                marker="o",
                linewidth=2,
                label=framework
            )

        ax.set_title(metric)
        ax.set_xlabel("Scenario Size")
        ax.set_ylabel("Score (%)")
        ax.set_ylim(0, 105)
        ax.grid(True, linestyle="--", alpha=0.3)
        ax.legend()

    fig.suptitle("Performance Across Scenario Sizes")
    save_chart("performance_across_scenario_sizes.png")


def generate_time_to_detection_chart():
    df = load_results(
        "time_to_detection.csv",
        {"Attack Type", "TTD_milliseconds"}
    ).copy()

    df["TTD_milliseconds"] = pd.to_numeric(
        df["TTD_milliseconds"], errors="raise"
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(df["Attack Type"].astype(str), df["TTD_milliseconds"])

    ax.set_xlabel("Attack Type")
    ax.set_ylabel("Time to Detection (milliseconds)")
    ax.set_title("Time to Detection by Attack Type")
    ax.tick_params(axis="x", labelrotation=30)

    for label in ax.get_xticklabels():
        label.set_horizontalalignment("right")

    ax.bar_label(bars, fmt="%.2f", padding=3, fontsize=8)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)

    save_chart("time_to_detection.png")

    if (df["TTD_milliseconds"] == 0).any():
        print("Warning: Zero detection latency exists in the input data.")


def generate_visibility_charts():
    df = load_results(
        "log_visibility_coverage.csv",
        {
            "Attack Chain",
            "Required Events",
            "Captured Events",
            "Coverage (%)"
        }
    ).copy()

    for column in ["Required Events", "Captured Events", "Coverage (%)"]:
        df[column] = pd.to_numeric(df[column], errors="raise")

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(df["Attack Chain"].astype(str), df["Coverage (%)"])

    ax.set_xlabel("Attack Chain")
    ax.set_ylabel("Log Visibility Coverage (%)")
    ax.set_title("Log Visibility Coverage by Attack Chain")
    ax.set_ylim(0, 110)
    ax.tick_params(axis="x", labelrotation=30)

    for label in ax.get_xticklabels():
        label.set_horizontalalignment("right")

    ax.bar_label(bars, fmt="%.1f%%", padding=3, fontsize=8)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)

    save_chart("log_visibility_coverage.png")

    x = list(range(len(df)))
    width = 0.36

    fig, ax = plt.subplots(figsize=(9, 5))

    required_bars = ax.bar(
        [position - width / 2 for position in x],
        df["Required Events"],
        width,
        label="Required Events"
    )

    captured_bars = ax.bar(
        [position + width / 2 for position in x],
        df["Captured Events"],
        width,
        label="Captured Events"
    )

    ax.set_xticks(x)
    ax.set_xticklabels(df["Attack Chain"].astype(str), rotation=30, ha="right")
    ax.set_xlabel("Attack Chain")
    ax.set_ylabel("Event Count")
    ax.set_title("Required vs Captured Events by Attack Chain")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)

    ax.bar_label(required_bars, fmt="%.0f", padding=2, fontsize=8)
    ax.bar_label(captured_bars, fmt="%.0f", padding=2, fontsize=8)

    save_chart("required_vs_captured_events.png")


def main():
    required_columns = {
        "Scenario Size",
        "Framework",
        "True Positive",
        "False Positive",
        "False Negative",
        "Precision",
        "Recall",
        "F1 Score"
    }

    try:
        df = load_results("large_scale_results.csv", required_columns)

        numeric_columns = [
            "Scenario Size",
            "True Positive",
            "False Positive",
            "False Negative",
            "Precision",
            "Recall",
            "F1 Score"
        ]

        for column in numeric_columns:
            df[column] = pd.to_numeric(df[column], errors="raise")

        generate_performance_chart(df)
        generate_detection_outcomes_chart(df)
        generate_performance_trends_chart(df)
        generate_time_to_detection_chart()
        generate_visibility_charts()

    except (FileNotFoundError, ValueError, KeyError, pd.errors.ParserError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print("All six graph files generated successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
