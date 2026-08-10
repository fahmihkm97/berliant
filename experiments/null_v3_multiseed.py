from statistics import mean

from berliant.bsib import (
    KeyedSimulator,
    load_scenario,
)
from berliant.discovery import SCIFDiscoveryV3

SCENARIO_PATH = "benchmarks/bsib_01/null/BSIB-NULL-001.yaml"

START_SEED = 3001
END_SEED = 4000
RUNS = END_SEED - START_SEED + 1

EXHAUSTIVE_EXECUTIONS = 37_000


def main() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    false_positive_runs = 0
    total_candidates = 0

    execution_counts: list[int] = []

    false_positive_examples: list[tuple[int, tuple[tuple[str, ...], ...]]] = []

    for seed in range(
        START_SEED,
        END_SEED + 1,
    ):
        simulator = KeyedSimulator(
            scenario,
            seed=seed,
        )

        engine = SCIFDiscoveryV3(
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

        report = engine.discover()

        candidates = tuple(candidate.capabilities for candidate in report.candidates)

        if candidates:
            false_positive_runs += 1
            total_candidates += len(candidates)

            if len(false_positive_examples) < 10:
                false_positive_examples.append(
                    (
                        seed,
                        candidates,
                    )
                )

        execution_counts.append(report.executions)

    mean_executions = mean(execution_counts)

    fp_rate = false_positive_runs / RUNS

    reduction = (1 - mean_executions / EXHAUSTIVE_EXECUTIONS) * 100

    print()
    print("BSIB-NULL-001 — SCIF V3")
    print("=" * 72)

    print(f"Seeds               : {START_SEED}-{END_SEED}")

    print(f"False-positive runs : {false_positive_runs}/{RUNS}")

    print(f"False-positive rate : {fp_rate:.2%}")

    print(f"Total candidates    : {total_candidates}")

    print(f"Mean executions     : {mean_executions:.1f}")

    print(f"Min executions      : {min(execution_counts)}")

    print(f"Max executions      : {max(execution_counts)}")

    print(f"Reduction exhaustive: {reduction:.2f}%")

    if false_positive_examples:
        print()
        print("FALSE-POSITIVE EXAMPLES")
        print("-" * 72)

        for seed, candidates in false_positive_examples:
            print(f"seed={seed} candidates={candidates}")


if __name__ == "__main__":
    main()
