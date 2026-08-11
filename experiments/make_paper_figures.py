import csv
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path("results/paper")
FIGURES = ROOT / "figures"

FIGURES.mkdir(
    parents=True,
    exist_ok=True,
)


def read_csv(
    filename: str,
) -> list[dict[str, str]]:
    with (ROOT / filename).open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def save_figure(
    filename: str,
) -> None:
    plt.tight_layout()

    plt.savefig(
        FIGURES / f"{filename}.pdf",
        bbox_inches="tight",
    )

    plt.savefig(
        FIGURES / f"{filename}.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()


# ============================================================
# Figure 1
# Method recovery comparison
# ============================================================

comparison = read_csv("method_comparison.csv")

scenarios = [
    "PAIR-002",
    "OVERLAP",
    "TRIPLE",
    "MIXED",
]

methods = [
    "SCIF V3",
    "Deletion",
    "Exhaustive",
    "SCIF V4",
]

recovery = {method: [] for method in methods}

for scenario in scenarios:
    for method in methods:
        row = next(
            item
            for item in comparison
            if (item["scenario"] == scenario and item["method"] == method)
        )

        recovery[method].append(float(row["recovery_rate"]) * 100)


fig, ax = plt.subplots(figsize=(9, 5.5))

width = 0.18

positions = list(range(len(scenarios)))

offsets = [
    -1.5 * width,
    -0.5 * width,
    0.5 * width,
    1.5 * width,
]

for method, offset in zip(
    methods,
    offsets,
    strict=True,
):
    values = recovery[method]

    bars = ax.bar(
        [position + offset for position in positions],
        values,
        width=width,
        label=method,
    )

    ax.bar_label(
        bars,
        fmt="%.0f",
        fontsize=8,
        padding=2,
    )

ax.set_xticks(positions)

ax.set_xticklabels(scenarios)

ax.set_ylim(
    0,
    112,
)

ax.set_ylabel("Exact recovery (%)")

ax.set_xlabel("Benchmark scenario")

ax.set_title("Exact Interaction Recovery by Discovery Method")

ax.legend(
    frameon=False,
    ncol=2,
)

ax.spines["top"].set_visible(False)

ax.spines["right"].set_visible(False)

save_figure("figure_1_recovery_comparison")


# ============================================================
# Figure 2
# Execution cost comparison
# ============================================================

executions = {method: [] for method in methods}

for scenario in scenarios:
    for method in methods:
        row = next(
            item
            for item in comparison
            if (item["scenario"] == scenario and item["method"] == method)
        )

        executions[method].append(float(row["mean_executions"]))


fig, ax = plt.subplots(figsize=(9, 5.5))

for method, offset in zip(
    methods,
    offsets,
    strict=True,
):
    bars = ax.bar(
        [position + offset for position in positions],
        executions[method],
        width=width,
        label=method,
    )

    ax.bar_label(
        bars,
        fmt="%.0f",
        fontsize=7,
        rotation=90,
        padding=2,
    )

ax.set_xticks(positions)

ax.set_xticklabels(scenarios)

ax.set_ylabel("Mean simulator executions")

ax.set_xlabel("Benchmark scenario")

ax.set_title("Discovery Cost by Method")

ax.legend(
    frameon=False,
    ncol=2,
)

ax.spines["top"].set_visible(False)

ax.spines["right"].set_visible(False)

save_figure("figure_2_execution_comparison")


# ============================================================
# Figure 3
# Scaling: SCIF V4 vs exhaustive
# ============================================================

scaling = read_csv("scaling_results.csv")

capabilities = [int(row["capabilities"]) for row in scaling]

v4_exec = [float(row["mean_executions"]) for row in scaling]

exhaustive_exec = [float(row["exhaustive_executions"]) for row in scaling]


fig, ax = plt.subplots(figsize=(8, 5.5))

ax.plot(
    capabilities,
    v4_exec,
    marker="o",
    linewidth=2,
    label="SCIF V4",
)

ax.plot(
    capabilities,
    exhaustive_exec,
    marker="o",
    linewidth=2,
    label="Exhaustive order-3",
)

ax.set_xticks(capabilities)

ax.set_xlabel("Number of capabilities")

ax.set_ylabel("Simulator executions")

ax.set_title("Scaling of Discovery Cost")

ax.legend(frameon=False)

ax.spines["top"].set_visible(False)

ax.spines["right"].set_visible(False)

save_figure("figure_3_scaling")


# ============================================================
# Figure 4
# Scaling reduction
# ============================================================

reductions = [float(row["reduction_percent"]) for row in scaling]


fig, ax = plt.subplots(figsize=(8, 5.5))

bars = ax.bar(
    [str(value) for value in capabilities],
    reductions,
)

ax.bar_label(
    bars,
    fmt="%.2f%%",
    padding=3,
)

ax.set_ylim(
    0,
    105,
)

ax.set_xlabel("Number of capabilities")

ax.set_ylabel("Execution reduction vs exhaustive (%)")

ax.set_title("SCIF V4 Execution Savings with Increasing Search Space")

ax.spines["top"].set_visible(False)

ax.spines["right"].set_visible(False)

save_figure("figure_4_scaling_reduction")


# ============================================================
# Figure 5
# Holdout recovery
# ============================================================

holdout = read_csv("holdout_results.csv")

holdout_scenarios = [row["scenario"] for row in holdout]

holdout_recovery = [float(row["recovery_rate"]) * 100 for row in holdout]


fig, ax = plt.subplots(figsize=(9, 5.5))

bars = ax.bar(
    holdout_scenarios,
    holdout_recovery,
)

ax.bar_label(
    bars,
    fmt="%.1f%%",
    padding=3,
)

ax.set_ylim(
    98.5,
    100.2,
)

ax.set_ylabel("Exact recovery (%)")

ax.set_xlabel("Holdout scenario")

ax.set_title("SCIF V4 Exact Recovery on 1,000-Seed Unseen Holdout")

ax.spines["top"].set_visible(False)

ax.spines["right"].set_visible(False)

save_figure("figure_5_holdout_recovery")


print("Paper figures generated:")

for path in sorted(FIGURES.iterdir()):
    print(
        " -",
        path,
    )
