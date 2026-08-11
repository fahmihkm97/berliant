from pathlib import Path
from statistics import mean

from berliant.bsib import (
    KeyedSimulator,
    load_scenario,
)
from berliant.discovery import (
    DeletionLocalizationBaseline,
    ExhaustiveDiscovery,
    SCIFDiscoveryV3,
    SCIFDiscoveryV4,
)

SCENARIOS = (
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
        2,
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
        2,
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
        3,
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
        3,
    ),
)


SEEDS = range(
    41001,
    41101,
)


for (
    name,
    scenario_path,
    expected_pairs,
    expected_higher,
    exhaustive_order,
) in SCENARIOS:
    scenario = load_scenario(scenario_path)

    results = {
        "SCIF V3": {
            "recovery": 0,
            "executions": [],
        },
        "Deletion": {
            "recovery": 0,
            "executions": [],
        },
        "Exhaustive": {
            "recovery": 0,
            "executions": [],
        },
        "SCIF V4": {
            "recovery": 0,
            "executions": [],
        },
    }

    for seed in SEEDS:
        # ----------------------------------------------------
        # SCIF V3
        # ----------------------------------------------------

        simulator = KeyedSimulator(
            scenario,
            seed=seed,
        )

        v3 = SCIFDiscoveryV3(
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
            seed=20260810 + seed,
        )

        v3_report = v3.discover()

        v3_pairs = {candidate.capabilities for candidate in v3_report.candidates}

        if v3_pairs == expected_pairs and not expected_higher:
            results["SCIF V3"]["recovery"] += 1

        results["SCIF V3"]["executions"].append(v3_report.executions)

        # ----------------------------------------------------
        # DELETION
        # ----------------------------------------------------

        simulator = KeyedSimulator(
            scenario,
            seed=seed,
        )

        deletion = DeletionLocalizationBaseline(
            invoke=simulator.invoke,
            capabilities=scenario.capabilities,
            trials_per_config=1000,
            min_failure=0.20,
            min_removal_drop=0.20,
        )

        deletion_report = deletion.discover()

        expected_single = None

        all_expected = expected_pairs | expected_higher

        if len(all_expected) == 1:
            expected_single = next(iter(all_expected))

        if expected_single is not None and deletion_report.candidate == expected_single:
            results["Deletion"]["recovery"] += 1

        results["Deletion"]["executions"].append(deletion_report.executions)

        # ----------------------------------------------------
        # EXHAUSTIVE
        # ----------------------------------------------------

        simulator = KeyedSimulator(
            scenario,
            seed=seed,
        )

        exhaustive = ExhaustiveDiscovery(
            invoke=simulator.invoke,
            capabilities=scenario.capabilities,
            max_order=exhaustive_order,
            trials_per_config=1000,
            min_joint_failure=0.15,
            min_jri=0.10,
        )

        exhaustive_report = exhaustive.discover()

        exhaustive_candidates = {
            candidate.capabilities for candidate in exhaustive_report.candidates
        }

        expected_all = expected_pairs | expected_higher

        if exhaustive_candidates == expected_all:
            results["Exhaustive"]["recovery"] += 1

        results["Exhaustive"]["executions"].append(exhaustive_report.executions)

        # ----------------------------------------------------
        # SCIF V4
        # ----------------------------------------------------

        simulator = KeyedSimulator(
            scenario,
            seed=seed,
        )

        v4 = SCIFDiscoveryV4(
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

        v4_report = v4.discover()

        v4_pairs = {
            candidate.capabilities for candidate in v4_report.pairwise_report.candidates
        }

        v4_higher: set[tuple[str, ...]] = set()

        if (
            v4_report.higher_order is not None
            and v4_report.higher_order.candidate is not None
        ):
            v4_higher.add(v4_report.higher_order.candidate)

        if v4_pairs == expected_pairs and v4_higher == expected_higher:
            results["SCIF V4"]["recovery"] += 1

        results["SCIF V4"]["executions"].append(v4_report.executions)

    total = len(tuple(SEEDS))

    print()
    print(name)
    print("=" * 78)

    print(f"{'Method':<16}{'Recovery':<18}{'Mean executions':<18}")

    print("-" * 78)

    for method, data in results.items():
        recovery = int(data["recovery"])

        executions = data["executions"]

        mean_executions = mean(executions)

        print(
            f"{method:<16}"
            f"{recovery}/{total} "
            f"({recovery / total:.1%})"
            f"{'':<5}"
            f"{mean_executions:<18.1f}"
        )
