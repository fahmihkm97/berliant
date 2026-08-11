from pathlib import Path
from statistics import mean, median

import numpy as np

from berliant.bsib import (
    KeyedSimulator,
    load_scenario,
)
from berliant.discovery import SCIFDiscoveryV4

SCENARIOS = (
    (
        "NULL",
        Path("benchmarks/bsib_01/null/BSIB-NULL-001.yaml"),
        (),
        (),
        37_000,
    ),
    (
        "PAIR-001",
        Path("benchmarks/bsib_01/easy/BSIB-PAIR-001.yaml"),
        (
            tuple(
                sorted(
                    (
                        "tools",
                        "structured_output",
                    )
                )
            ),
        ),
        (),
        37_000,
    ),
    (
        "PAIR-002",
        Path("benchmarks/bsib_01/easy/BSIB-PAIR-002.yaml"),
        (
            tuple(
                sorted(
                    (
                        "tools",
                        "streaming",
                    )
                )
            ),
        ),
        (),
        37_000,
    ),
    (
        "PAIR-003",
        Path("benchmarks/bsib_01/medium/BSIB-PAIR-003.yaml"),
        (
            tuple(
                sorted(
                    (
                        "parallel_tools",
                        "strict_schema",
                    )
                )
            ),
        ),
        (),
        37_000,
    ),
    (
        "OVERLAP",
        Path("benchmarks/bsib_01/higher_order/BSIB-OVERLAP-001.yaml"),
        (
            tuple(
                sorted(
                    (
                        "tools",
                        "streaming",
                    )
                )
            ),
            tuple(
                sorted(
                    (
                        "streaming",
                        "strict_schema",
                    )
                )
            ),
        ),
        (),
        37_000,
    ),
    (
        "TRIPLE",
        Path("benchmarks/bsib_01/higher_order/BSIB-TRIPLE-001.yaml"),
        (),
        (
            tuple(
                sorted(
                    (
                        "tools",
                        "streaming",
                        "strict_schema",
                    )
                )
            ),
        ),
        93_000,
    ),
    (
        "MIXED",
        Path("benchmarks/bsib_01/mixed/BSIB-MIXED-001.yaml"),
        (
            tuple(
                sorted(
                    (
                        "tools",
                        "streaming",
                    )
                )
            ),
        ),
        (
            tuple(
                sorted(
                    (
                        "reasoning",
                        "strict_schema",
                        "multimodal",
                    )
                )
            ),
        ),
        93_000,
    ),
)


SEEDS = range(
    31001,
    32001,
)


def percentile(
    values: list[int],
    q: float,
) -> float:
    return float(
        np.percentile(
            values,
            q,
        )
    )


for (
    name,
    scenario_path,
    expected_pairs,
    expected_higher_order,
    exhaustive_executions,
) in SCENARIOS:
    scenario = load_scenario(scenario_path)

    expected_pair_set = set(expected_pairs)

    expected_higher_set = set(expected_higher_order)

    exact_recovery = 0
    pair_recovery = 0
    residual_correct = 0
    higher_order_recovery = 0
    false_positive_runs = 0

    executions: list[int] = []

    for seed in SEEDS:
        simulator = KeyedSimulator(
            scenario,
            seed=seed,
        )

        engine = SCIFDiscoveryV4(
            invoke=simulator.invoke,
            capabilities=scenario.capabilities,
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

        report = engine.discover()

        discovered_pairs = {
            candidate.capabilities for candidate in report.pairwise_report.candidates
        }

        discovered_higher: set[tuple[str, ...]] = set()

        if (
            report.higher_order is not None
            and report.higher_order.candidate is not None
        ):
            discovered_higher.add(report.higher_order.candidate)

        expected_residual = bool(expected_higher_set)

        if discovered_pairs == expected_pair_set:
            pair_recovery += 1

        if report.residual.residual_detected == expected_residual:
            residual_correct += 1

        if discovered_higher == expected_higher_set:
            higher_order_recovery += 1

        exact = (
            discovered_pairs == expected_pair_set
            and discovered_higher == expected_higher_set
            and (report.residual.residual_detected == expected_residual)
        )

        if exact:
            exact_recovery += 1

        unexpected_pairs = discovered_pairs - expected_pair_set

        unexpected_higher = discovered_higher - expected_higher_set

        if unexpected_pairs or unexpected_higher:
            false_positive_runs += 1

        executions.append(report.executions)

    total = len(executions)

    mean_exec = mean(executions)

    reduction = (1 - mean_exec / exhaustive_executions) * 100

    print()
    print(name)
    print("=" * 76)

    print(f"Runs                   : {total}")

    print(
        "Exact recovery         : "
        f"{exact_recovery}/{total} "
        f"({exact_recovery / total:.1%})"
    )

    print(
        "Pair recovery          : "
        f"{pair_recovery}/{total} "
        f"({pair_recovery / total:.1%})"
    )

    print(
        "Residual classification: "
        f"{residual_correct}/{total} "
        f"({residual_correct / total:.1%})"
    )

    print(
        "Higher-order recovery  : "
        f"{higher_order_recovery}/{total} "
        f"({higher_order_recovery / total:.1%})"
    )

    print(f"False-positive runs    : {false_positive_runs}/{total}")

    print(f"Executions mean        : {mean_exec:.1f}")

    print(f"Executions median      : {median(executions):.1f}")

    print(f"Executions min         : {min(executions)}")

    print(f"Executions max         : {max(executions)}")

    print(f"Executions P95         : {percentile(executions, 95):.1f}")

    print(f"Reduction vs exhaustive: {reduction:.2f}%")
