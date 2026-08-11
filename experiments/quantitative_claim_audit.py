import csv
from pathlib import Path
from typing import Any

RESULTS = Path("results/paper")
MANUSCRIPT = Path("paper/manuscript.md")


def read_csv(
    filename: str,
) -> list[dict[str, str]]:
    path = RESULTS / filename

    with path.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def find_row(
    rows: list[dict[str, str]],
    **criteria: Any,
) -> dict[str, str]:
    for row in rows:
        matched = True

        for key, expected in criteria.items():
            actual = row.get(key)

            if str(actual) != str(expected):
                matched = False
                break

        if matched:
            return row

    raise RuntimeError(f"Row not found: {criteria}")


def check_equal(
    label: str,
    actual: Any,
    expected: Any,
) -> None:
    if actual != expected:
        raise RuntimeError(f"{label}: expected {expected!r}, got {actual!r}")

    print(f"PASS: {label}")


def check_close(
    label: str,
    actual: float,
    expected: float,
    tolerance: float = 1e-6,
) -> None:
    if abs(actual - expected) > tolerance:
        raise RuntimeError(f"{label}: expected {expected}, got {actual}")

    print(f"PASS: {label}")


holdout = read_csv("holdout_results.csv")

comparison = read_csv("method_comparison.csv")

scaling = read_csv("scaling_results.csv")

holdout_ci = read_csv("holdout_results_ci.csv")


print("=== Holdout audit ===")

total_runs = sum(int(row["runs"]) for row in holdout)

total_recovery = sum(int(row["exact_recovery"]) for row in holdout)

total_false_positive = sum(int(row["false_positive_runs"]) for row in holdout)

check_equal(
    "holdout total runs",
    total_runs,
    7000,
)

check_equal(
    "holdout exact recoveries",
    total_recovery,
    6999,
)

check_equal(
    "holdout observed FP runs",
    total_false_positive,
    0,
)

overall_rate = total_recovery / total_runs

check_close(
    "overall recovery rate",
    overall_rate,
    6999 / 7000,
)


pair002 = find_row(
    holdout,
    scenario="PAIR-002",
)

check_equal(
    "PAIR-002 runs",
    int(pair002["runs"]),
    1000,
)

check_equal(
    "PAIR-002 recoveries",
    int(pair002["exact_recovery"]),
    999,
)

check_close(
    "PAIR-002 recovery rate",
    float(pair002["recovery_rate"]),
    0.999,
)

check_close(
    "PAIR-002 mean executions",
    float(pair002["mean_executions"]),
    10946.2,
)

check_close(
    "PAIR-002 reduction",
    float(pair002["reduction_percent"]),
    70.42,
)


print()
print("=== Confidence interval audit ===")

overall_ci = find_row(
    holdout_ci,
    scenario="OVERALL",
)

check_close(
    "overall CI recovery",
    float(overall_ci["recovery_percent"]),
    99.9857,
    tolerance=0.0001,
)

check_close(
    "overall CI lower",
    float(overall_ci["ci95_lower_percent"]),
    99.9191,
    tolerance=0.0001,
)

check_close(
    "overall CI upper",
    float(overall_ci["ci95_upper_percent"]),
    99.9975,
    tolerance=0.0001,
)


print()
print("=== Method comparison audit ===")


def comparison_row(
    scenario: str,
    method_fragment: str,
) -> dict[str, str]:
    for row in comparison:
        if (
            row["scenario"] == scenario
            and method_fragment.lower() in row["method"].lower()
        ):
            return row

    raise RuntimeError(f"Comparison row not found: {scenario}, {method_fragment}")


checks = (
    (
        "PAIR-002",
        "V4",
        1.0,
        10900.0,
    ),
    (
        "OVERLAP",
        "V4",
        1.0,
        13100.0,
    ),
    (
        "TRIPLE",
        "V4",
        1.0,
        17700.0,
    ),
    (
        "MIXED",
        "V4",
        1.0,
        22800.0,
    ),
    (
        "TRIPLE",
        "V3",
        0.0,
        3700.0,
    ),
    (
        "MIXED",
        "V3",
        0.0,
        7800.0,
    ),
    (
        "OVERLAP",
        "Deletion",
        0.0,
        9000.0,
    ),
    (
        "MIXED",
        "Deletion",
        0.0,
        9000.0,
    ),
)

for (
    scenario,
    method,
    recovery,
    executions,
) in checks:
    row = comparison_row(
        scenario,
        method,
    )

    check_close(
        f"{scenario} {method} recovery",
        float(row["recovery_rate"]),
        recovery,
    )

    check_close(
        f"{scenario} {method} executions",
        float(row["mean_executions"]),
        executions,
    )


print()
print("=== Scaling audit ===")

for row in scaling:
    check_close(
        (f"scaling recovery N={row['capabilities']}"),
        float(row["exact_recovery"]),
        1.0,
    )


scale8 = find_row(
    scaling,
    capabilities="8",
)

scale20 = find_row(
    scaling,
    capabilities="20",
)

check_close(
    "N=8 reduction",
    float(scale8["reduction_percent"]),
    75.48,
)

check_close(
    "N=20 reduction",
    float(scale20["reduction_percent"]),
    96.14,
)

check_close(
    "N=8 executions",
    float(scale8["mean_executions"]),
    22800.0,
)

check_close(
    "N=20 executions",
    float(scale20["mean_executions"]),
    52200.0,
)


print()
print("=== Manuscript claim presence ===")

text = MANUSCRIPT.read_text(encoding="utf-8")

required_claims = (
    "99.9857",
    "99.9191",
    "99.9975",
    "999/1000",
    "75.48%",
    "96.14%",
    "20/20",
)

for claim in required_claims:
    if claim not in text:
        raise RuntimeError(
            f"Required quantitative claim not found in manuscript: {claim}"
        )

    print(
        "PASS: manuscript contains",
        claim,
    )


print()
print("QUANTITATIVE CLAIM AUDIT PASSED")
