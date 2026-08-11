from pathlib import Path
from statistics import mean

from berliant.bsib import (
    KeyedSimulator,
    load_scenario,
)
from berliant.discovery import SCIFDiscoveryV4

SCENARIOS = (
    (
        "NULL",
        Path("benchmarks/bsib_01/null/BSIB-NULL-001.yaml"),
        set(),
        set(),
    ),
    (
        "PAIR-002",
        Path("benchmarks/bsib_01/easy/BSIB-PAIR-002.yaml"),
        {
            tuple(
                sorted(
                    (
                        "tools",
                        "streaming",
                    )
                )
            )
        },
        set(),
    ),
    (
        "TRIPLE",
        Path("benchmarks/bsib_01/higher_order/BSIB-TRIPLE-001.yaml"),
        set(),
        {
            tuple(
                sorted(
                    (
                        "tools",
                        "streaming",
                        "strict_schema",
                    )
                )
            )
        },
    ),
    (
        "MIXED",
        Path("benchmarks/bsib_01/mixed/BSIB-MIXED-001.yaml"),
        {
            tuple(
                sorted(
                    (
                        "tools",
                        "streaming",
                    )
                )
            )
        },
        {
            tuple(
                sorted(
                    (
                        "reasoning",
                        "strict_schema",
                        "multimodal",
                    )
                )
            )
        },
    ),
)


SETTINGS = (
    (
        "BASELINE",
        100,
        0.10,
        0.10,
    ),
    (
        "INITIAL-50",
        50,
        0.10,
        0.10,
    ),
    (
        "INITIAL-200",
        200,
        0.10,
        0.10,
    ),
    (
        "RESIDUAL-0.05",
        100,
        0.05,
        0.10,
    ),
    (
        "RESIDUAL-0.15",
        100,
        0.15,
        0.10,
    ),
    (
        "REMOVAL-0.05",
        100,
        0.10,
        0.05,
    ),
    (
        "REMOVAL-0.15",
        100,
        0.10,
        0.15,
    ),
)


SEEDS = range(
    61001,
    61101,
)


for (
    scenario_name,
    scenario_path,
    expected_pairs,
    expected_higher,
) in SCENARIOS:
    scenario = load_scenario(scenario_path)

    print()
    print(scenario_name)
    print("=" * 100)

    print(
        f"{'Setting':<20}{'Exact':<18}{'Residual':<18}{'FP runs':<14}{'Mean exec':<14}"
    )

    print("-" * 100)

    for (
        setting_name,
        initial_trials,
        min_residual_increment,
        min_removal_drop,
    ) in SETTINGS:
        exact_recovery = 0
        residual_correct = 0
        false_positive_runs = 0
        executions: list[int] = []

        expected_residual = bool(expected_higher)

        for seed in SEEDS:
            simulator = KeyedSimulator(
                scenario,
                seed=seed,
            )

            engine = SCIFDiscoveryV4(
                invoke=simulator.invoke,
                capabilities=scenario.capabilities,
                initial_trials=initial_trials,
                screening_retest_trials=300,
                screening_probability_threshold=0.20,
                confirm_trials=1500,
                subset_confirm_trials=1000,
                min_joint_failure=0.15,
                min_jri=0.10,
                confidence_threshold=0.95,
                residual_trials=1000,
                min_residual_failure=0.15,
                min_residual_increment=(min_residual_increment),
                higher_order_trials=1000,
                higher_order_min_failure=0.15,
                higher_order_min_removal_drop=(min_removal_drop),
                higher_order_min_candidate_size=3,
                seed=20260810 + seed,
            )

            report = engine.discover()

            discovered_pairs = {
                candidate.capabilities
                for candidate in report.pairwise_report.candidates
            }

            discovered_higher: set[tuple[str, ...]] = set()

            if (
                report.higher_order is not None
                and report.higher_order.candidate is not None
            ):
                discovered_higher.add(report.higher_order.candidate)

            residual_ok = report.residual.residual_detected == expected_residual

            if residual_ok:
                residual_correct += 1

            exact = (
                discovered_pairs == expected_pairs
                and discovered_higher == expected_higher
                and residual_ok
            )

            if exact:
                exact_recovery += 1

            unexpected_pairs = discovered_pairs - expected_pairs

            unexpected_higher = discovered_higher - expected_higher

            if unexpected_pairs or unexpected_higher:
                false_positive_runs += 1

            executions.append(report.executions)

        total = len(executions)

        print(
            f"{setting_name:<20}"
            f"{exact_recovery}/{total} "
            f"({exact_recovery / total:.1%})"
            f"{'':<4}"
            f"{residual_correct}/{total} "
            f"({residual_correct / total:.1%})"
            f"{'':<4}"
            f"{false_positive_runs}/{total}"
            f"{'':<7}"
            f"{mean(executions):<14.1f}"
        )
