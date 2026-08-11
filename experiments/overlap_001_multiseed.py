from statistics import mean

from berliant.bsib import (
    KeyedSimulator,
    load_scenario,
)
from berliant.discovery import (
    DeletionLocalizationBaseline,
    SCIFDiscoveryV3,
)

SCENARIO_PATH = "benchmarks/bsib_01/higher_order/BSIB-OVERLAP-001.yaml"

FAULT_A = tuple(
    sorted(
        (
            "tools",
            "streaming",
        )
    )
)

FAULT_B = tuple(
    sorted(
        (
            "streaming",
            "strict_schema",
        )
    )
)

TRUTH = {
    FAULT_A,
    FAULT_B,
}

START_SEED = 11001
END_SEED = 12000
RUNS = END_SEED - START_SEED + 1

EXHAUSTIVE_EXECUTIONS = 37_000


def main() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    v3_both_recovered = 0
    v3_partial = 0
    v3_neither = 0
    v3_false_positive_runs = 0

    v3_execution_counts: list[int] = []

    deletion_none = 0
    deletion_candidate_runs = 0

    missed_examples: list[
        tuple[
            int,
            tuple[tuple[str, ...], ...],
        ]
    ] = []

    fp_examples: list[
        tuple[
            int,
            tuple[tuple[str, ...], ...],
        ]
    ] = []

    deletion_examples: list[tuple[int, tuple[str, ...]]] = []

    for seed in range(
        START_SEED,
        END_SEED + 1,
    ):
        v3_simulator = KeyedSimulator(
            scenario,
            seed=seed,
        )

        v3 = SCIFDiscoveryV3(
            invoke=v3_simulator.invoke,
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

        discovered = {candidate.capabilities for candidate in v3_report.candidates}

        recovered_truth = discovered.intersection(TRUTH)

        if recovered_truth == TRUTH:
            v3_both_recovered += 1
        elif recovered_truth:
            v3_partial += 1

            if len(missed_examples) < 10:
                missed_examples.append(
                    (
                        seed,
                        tuple(sorted(discovered)),
                    )
                )
        else:
            v3_neither += 1

            if len(missed_examples) < 10:
                missed_examples.append(
                    (
                        seed,
                        tuple(sorted(discovered)),
                    )
                )

        unexpected = discovered.difference(TRUTH)

        if unexpected:
            v3_false_positive_runs += 1

            if len(fp_examples) < 10:
                fp_examples.append(
                    (
                        seed,
                        tuple(sorted(unexpected)),
                    )
                )

        v3_execution_counts.append(v3_report.executions)

        deletion_simulator = KeyedSimulator(
            scenario,
            seed=seed,
        )

        deletion = DeletionLocalizationBaseline(
            invoke=(deletion_simulator.invoke),
            capabilities=(scenario.capabilities),
            trials_per_config=1000,
            min_failure=0.20,
            min_removal_drop=0.20,
        )

        deletion_report = deletion.discover()

        if deletion_report.candidate is None:
            deletion_none += 1
        else:
            deletion_candidate_runs += 1

            if len(deletion_examples) < 10:
                deletion_examples.append(
                    (
                        seed,
                        deletion_report.candidate,
                    )
                )

    mean_v3_exec = mean(v3_execution_counts)

    reduction = (1 - mean_v3_exec / EXHAUSTIVE_EXECUTIONS) * 100

    print()
    print("BSIB-OVERLAP-001 — MULTISEED")
    print("=" * 72)

    print(f"Seeds                    : {START_SEED}-{END_SEED}")

    print()
    print("SCIF V3")
    print("-" * 72)

    print(
        f"Both faults recovered    : "
        f"{v3_both_recovered}/{RUNS} "
        f"({v3_both_recovered / RUNS:.2%})"
    )

    print(f"Partial recovery         : {v3_partial}/{RUNS} ({v3_partial / RUNS:.2%})")

    print(f"Neither recovered        : {v3_neither}/{RUNS} ({v3_neither / RUNS:.2%})")

    print(
        f"False-positive runs      : "
        f"{v3_false_positive_runs}/{RUNS} "
        f"({v3_false_positive_runs / RUNS:.2%})"
    )

    print(f"Mean executions          : {mean_v3_exec:.1f}")

    print(f"Min executions           : {min(v3_execution_counts)}")

    print(f"Max executions           : {max(v3_execution_counts)}")

    print(f"Reduction vs exhaustive  : {reduction:.2f}%")

    print()
    print("DELETION BASELINE")
    print("-" * 72)

    print(
        f"candidate=None           : "
        f"{deletion_none}/{RUNS} "
        f"({deletion_none / RUNS:.2%})"
    )

    print(
        f"candidate produced       : "
        f"{deletion_candidate_runs}/{RUNS} "
        f"({deletion_candidate_runs / RUNS:.2%})"
    )

    if missed_examples:
        print()
        print("SCIF RECOVERY EXAMPLES")
        print("-" * 72)

        for seed, candidates in missed_examples:
            print(f"seed={seed} candidates={candidates}")

    if fp_examples:
        print()
        print("SCIF FALSE-POSITIVE EXAMPLES")
        print("-" * 72)

        for seed, candidates in fp_examples:
            print(f"seed={seed} unexpected={candidates}")

    if deletion_examples:
        print()
        print("DELETION CANDIDATE EXAMPLES")
        print("-" * 72)

        for seed, candidate in deletion_examples:
            print(f"seed={seed} candidate={candidate}")


if __name__ == "__main__":
    main()
