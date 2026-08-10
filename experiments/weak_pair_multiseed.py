from statistics import mean

from berliant.bsib import Simulator, load_scenario
from berliant.discovery import SCIFDiscovery

SCENARIO_PATH = "benchmarks/bsib_01/easy/BSIB-PAIR-002.yaml"

EXPECTED = tuple(
    sorted(
        (
            "tools",
            "streaming",
        )
    )
)

RUNS = 30


def main() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    exact_recoveries = 0
    false_positive_runs = 0
    execution_counts: list[int] = []

    print()
    print("BSIB-PAIR-002 MULTI-SEED EXPERIMENT")
    print("=" * 72)

    for seed in range(1, RUNS + 1):
        simulator = Simulator(
            scenario,
            seed=seed,
        )

        engine = SCIFDiscovery(
            invoke=simulator.invoke,
            capabilities=scenario.capabilities,
            initial_trials=100,
            confirm_trials=1500,
            min_joint_failure=0.15,
            min_jri=0.10,
            confidence_threshold=0.95,
            seed=20260810 + seed,
        )

        report = engine.discover()

        discovered = {candidate.capabilities for candidate in report.candidates}

        found_expected = EXPECTED in discovered

        if found_expected:
            exact_recoveries += 1

        unexpected = discovered.difference({EXPECTED})

        if unexpected:
            false_positive_runs += 1

        execution_counts.append(report.executions)

        status = "FOUND" if found_expected else "MISSED"

        print(
            f"seed={seed:02d} "
            f"{status:<7} "
            f"candidates={len(discovered):<2} "
            f"executions={report.executions}"
        )

    recovery_rate = exact_recoveries / RUNS

    false_positive_rate = false_positive_runs / RUNS

    print()
    print("SUMMARY")
    print("-" * 72)

    print(f"Exact recoveries    : {exact_recoveries}/{RUNS}")

    print(f"Recovery rate       : {recovery_rate:.2%}")

    print(f"False-positive runs : {false_positive_runs}/{RUNS}")

    print(f"False-positive rate : {false_positive_rate:.2%}")

    print(f"Mean executions     : {mean(execution_counts):.1f}")


if __name__ == "__main__":
    main()
