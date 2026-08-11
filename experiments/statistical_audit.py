import csv
import math
from pathlib import Path

ROOT = Path("results/paper")

Z_95 = 1.959963984540054


def wilson_interval(
    successes: int,
    trials: int,
    z: float = Z_95,
) -> tuple[float, float]:
    if trials <= 0:
        raise ValueError("trials must be positive")

    p = successes / trials

    denominator = 1 + z**2 / trials

    center = (p + z**2 / (2 * trials)) / denominator

    half_width = (
        z * math.sqrt((p * (1 - p) + z**2 / (4 * trials)) / trials) / denominator
    )

    return (
        center - half_width,
        center + half_width,
    )


def percent(
    value: float,
) -> float:
    return value * 100


def write_holdout_ci() -> None:
    input_path = ROOT / "holdout_results.csv"

    output_path = ROOT / "holdout_results_ci.csv"

    with input_path.open(
        encoding="utf-8",
        newline="",
    ) as source:
        rows = list(csv.DictReader(source))

    fieldnames = [
        "scenario",
        "runs",
        "exact_recovery",
        "recovery_percent",
        "ci95_lower_percent",
        "ci95_upper_percent",
        "false_positive_runs",
        "mean_executions",
    ]

    with output_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as target:
        writer = csv.DictWriter(
            target,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        total_success = 0
        total_runs = 0

        for row in rows:
            runs = int(row["runs"])

            success = int(row["exact_recovery"])

            lower, upper = wilson_interval(
                success,
                runs,
            )

            writer.writerow(
                {
                    "scenario": row["scenario"],
                    "runs": runs,
                    "exact_recovery": (success),
                    "recovery_percent": (f"{percent(success / runs):.4f}"),
                    "ci95_lower_percent": (f"{percent(lower):.4f}"),
                    "ci95_upper_percent": (f"{percent(upper):.4f}"),
                    "false_positive_runs": row["false_positive_runs"],
                    "mean_executions": row["mean_executions"],
                }
            )

            total_success += success

            total_runs += runs

        lower, upper = wilson_interval(
            total_success,
            total_runs,
        )

        writer.writerow(
            {
                "scenario": ("OVERALL"),
                "runs": total_runs,
                "exact_recovery": (total_success),
                "recovery_percent": (f"{percent(total_success / total_runs):.4f}"),
                "ci95_lower_percent": (f"{percent(lower):.4f}"),
                "ci95_upper_percent": (f"{percent(upper):.4f}"),
                "false_positive_runs": (0),
                "mean_executions": "",
            }
        )


def write_comparison_ci() -> None:
    input_path = ROOT / "method_comparison.csv"

    output_path = ROOT / "method_comparison_ci.csv"

    with input_path.open(
        encoding="utf-8",
        newline="",
    ) as source:
        rows = list(csv.DictReader(source))

    fieldnames = [
        "scenario",
        "method",
        "runs",
        "recoveries",
        "recovery_percent",
        "ci95_lower_percent",
        "ci95_upper_percent",
        "mean_executions",
    ]

    with output_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as target:
        writer = csv.DictWriter(
            target,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for row in rows:
            runs = 100

            rate = float(row["recovery_rate"])

            recoveries = round(rate * runs)

            lower, upper = wilson_interval(
                recoveries,
                runs,
            )

            writer.writerow(
                {
                    "scenario": row["scenario"],
                    "method": row["method"],
                    "runs": runs,
                    "recoveries": (recoveries),
                    "recovery_percent": (f"{percent(rate):.4f}"),
                    "ci95_lower_percent": (f"{percent(lower):.4f}"),
                    "ci95_upper_percent": (f"{percent(upper):.4f}"),
                    "mean_executions": row["mean_executions"],
                }
            )


def write_scaling_ci() -> None:
    input_path = ROOT / "scaling_results.csv"

    output_path = ROOT / "scaling_results_ci.csv"

    with input_path.open(
        encoding="utf-8",
        newline="",
    ) as source:
        rows = list(csv.DictReader(source))

    fieldnames = [
        "capabilities",
        "runs",
        "recoveries",
        "recovery_percent",
        "ci95_lower_percent",
        "ci95_upper_percent",
        "mean_executions",
        "exhaustive_executions",
        "reduction_percent",
        "mean_seconds",
    ]

    with output_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as target:
        writer = csv.DictWriter(
            target,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for row in rows:
            runs = int(row["runs"])

            rate = float(row["exact_recovery"])

            recoveries = round(rate * runs)

            lower, upper = wilson_interval(
                recoveries,
                runs,
            )

            writer.writerow(
                {
                    "capabilities": row["capabilities"],
                    "runs": runs,
                    "recoveries": (recoveries),
                    "recovery_percent": (f"{percent(rate):.4f}"),
                    "ci95_lower_percent": (f"{percent(lower):.4f}"),
                    "ci95_upper_percent": (f"{percent(upper):.4f}"),
                    "mean_executions": row["mean_executions"],
                    "exhaustive_executions": row["exhaustive_executions"],
                    "reduction_percent": row["reduction_percent"],
                    "mean_seconds": row["mean_seconds"],
                }
            )


write_holdout_ci()
write_comparison_ci()
write_scaling_ci()

print("Statistical audit complete.")

print()

for path in (
    ROOT / "holdout_results_ci.csv",
    ROOT / "method_comparison_ci.csv",
    ROOT / "scaling_results_ci.csv",
):
    print(path)
