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
        "OVERLAP",
        Path("benchmarks/bsib_01/higher_order/BSIB-OVERLAP-001.yaml"),
        {
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


SEEDS = range(
    51001,
    51101,
)


for (
    name,
    scenario_path,
    expected_pairs,
    expected_higher,
) in SCENARIOS:
    scenario = load_scenario(scenario_path)

    v3_full_exact = 0
    residual_stage_correct = 0
    v4_full_exact = 0

    false_escalations = 0
    missed_escalations = 0
    false_higher_order = 0

    v3_executions: list[int] = []
    residual_executions: list[int] = []
    v4_executions: list[int] = []

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

        expected_residual = bool(expected_higher)

        # ----------------------------------------------------
        # Stage A: V3 pairwise only
        #
        # Full recovery is possible only when the scenario
        # contains no higher-order interaction.
        # ----------------------------------------------------

        v3_exact = discovered_pairs == expected_pairs and not expected_higher

        if v3_exact:
            v3_full_exact += 1

        # ----------------------------------------------------
        # Stage B: V3 + residual-risk detection
        #
        # This stage does not yet localize the triple.
        # Success means:
        # - pairwise result is correct
        # - escalation decision is correct
        # ----------------------------------------------------

        residual_correct = discovered_pairs == expected_pairs and (
            report.residual.residual_detected == expected_residual
        )

        if residual_correct:
            residual_stage_correct += 1

        if not expected_residual and report.residual.residual_detected:
            false_escalations += 1

        if expected_residual and not report.residual.residual_detected:
            missed_escalations += 1

        # ----------------------------------------------------
        # Stage C: Full V4
        # ----------------------------------------------------

        v4_exact = (
            discovered_pairs == expected_pairs
            and discovered_higher == expected_higher
            and (report.residual.residual_detected == expected_residual)
        )

        if v4_exact:
            v4_full_exact += 1

        unexpected_higher = discovered_higher - expected_higher

        if unexpected_higher:
            false_higher_order += 1

        # ----------------------------------------------------
        # Execution accounting
        # ----------------------------------------------------

        pair_exec = report.pairwise_report.executions

        residual_exec = pair_exec + report.residual.executions

        v3_executions.append(pair_exec)

        residual_executions.append(residual_exec)

        v4_executions.append(report.executions)

    total = len(v4_executions)

    print()
    print(name)
    print("=" * 82)

    print(f"{'Stage':<24}{'Success':<22}{'Mean executions':<20}")

    print("-" * 82)

    print(
        f"{'V3 pairwise only':<24}"
        f"{v3_full_exact}/{total} "
        f"({v3_full_exact / total:.1%})"
        f"{'':<5}"
        f"{mean(v3_executions):<20.1f}"
    )

    print(
        f"{'V3 + residual':<24}"
        f"{residual_stage_correct}/{total} "
        f"({residual_stage_correct / total:.1%})"
        f"{'':<5}"
        f"{mean(residual_executions):<20.1f}"
    )

    print(
        f"{'Full V4':<24}"
        f"{v4_full_exact}/{total} "
        f"({v4_full_exact / total:.1%})"
        f"{'':<5}"
        f"{mean(v4_executions):<20.1f}"
    )

    print()
    print(
        "False escalations     :",
        f"{false_escalations}/{total}",
    )

    print(
        "Missed escalations    :",
        f"{missed_escalations}/{total}",
    )

    print(
        "False higher-order    :",
        f"{false_higher_order}/{total}",
    )
