from math import comb
from pathlib import Path
from statistics import mean
from time import perf_counter

import numpy as np

from berliant.bsib import (
    KeyedSimulator,
    load_scenario,
)
from berliant.discovery import SCIFDiscoveryV4

SIZES = (
    8,
    12,
    16,
    20,
)


SEEDS = range(
    71001,
    71021,
)


EXPECTED_PAIR = tuple(
    sorted(
        (
            "tools",
            "streaming",
        )
    )
)


EXPECTED_TRIPLE = tuple(
    sorted(
        (
            "reasoning",
            "strict_schema",
            "multimodal",
        )
    )
)


def percentile(
    values: list[float],
    q: float,
) -> float:
    return float(
        np.percentile(
            values,
            q,
        )
    )


print()
print("SCIF V4 SCALING STUDY")
print("=" * 110)

print(
    f"{'N':<6}"
    f"{'Exact':<18}"
    f"{'Mean exec':<16}"
    f"{'P95 exec':<16}"
    f"{'Exhaustive':<16}"
    f"{'Reduction':<14}"
    f"{'Mean sec':<12}"
)

print("-" * 110)


for size in SIZES:
    scenario_path = Path(f"benchmarks/bsib_01/scaling/BSIB-SCALE-{size:02d}.yaml")

    scenario = load_scenario(scenario_path)

    exact_recovery = 0

    executions: list[int] = []

    durations: list[float] = []

    for seed in SEEDS:
        simulator = KeyedSimulator(
            scenario,
            seed=seed,
        )

        engine = SCIFDiscoveryV4(
            invoke=simulator.invoke,
            capabilities=(scenario.capabilities),
            initial_trials=100,
            screening_retest_trials=300,
            screening_probability_threshold=0.20,
            confirm_trials=1500,
            subset_confirm_trials=1000,
            min_joint_failure=0.15,
            min_jri=0.10,
            confidence_threshold=0.95,
            residual_trials=1000,
            min_residual_failure=0.15,
            min_residual_increment=0.10,
            higher_order_trials=1000,
            higher_order_min_failure=0.15,
            higher_order_min_removal_drop=0.10,
            higher_order_min_candidate_size=3,
            seed=20260810 + seed,
        )

        started = perf_counter()

        report = engine.discover()

        durations.append(perf_counter() - started)

        discovered_pairs = {
            candidate.capabilities for candidate in report.pairwise_report.candidates
        }

        higher_order = None

        if report.higher_order is not None:
            higher_order = report.higher_order.candidate

        exact = (
            discovered_pairs == {EXPECTED_PAIR}
            and higher_order == EXPECTED_TRIPLE
            and report.residual.residual_detected
        )

        if exact:
            exact_recovery += 1

        executions.append(report.executions)

    total = len(executions)

    exhaustive_configurations = (
        1
        + size
        + comb(
            size,
            2,
        )
        + comb(
            size,
            3,
        )
    )

    exhaustive_executions = exhaustive_configurations * 1000

    mean_exec = mean(executions)

    reduction = (1 - mean_exec / exhaustive_executions) * 100

    print(
        f"{size:<6}"
        f"{exact_recovery}/{total} "
        f"({exact_recovery / total:.0%})"
        f"{'':<4}"
        f"{mean_exec:<16.1f}"
        f"{percentile(executions, 95):<16.1f}"
        f"{exhaustive_executions:<16}"
        f"{reduction:<14.2f}"
        f"{mean(durations):<12.4f}"
    )
