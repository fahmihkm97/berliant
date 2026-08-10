from collections import Counter
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

RUNS = 100


def main() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    outcomes: Counter[str] = Counter()
    executions: list[int] = []

    print()
    print("SCIF v0.0.1 WEAK-FAULT DIAGNOSTIC")
    print("=" * 76)

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

        executions.append(report.executions)

        discovered = {candidate.capabilities for candidate in report.candidates}

        expected_stats = report.stats[EXPECTED]

        if EXPECTED in discovered:
            outcome = "RECOVERED"

        elif expected_stats.trials == 100:
            outcome = "SCREENING_MISS"

        else:
            outcome = "CONFIRMATION_MISS"

        outcomes[outcome] += 1

        print(
            f"seed={seed:03d} "
            f"{outcome:<18} "
            f"pair_trials={expected_stats.trials:<4} "
            f"pair_rate={expected_stats.failure_rate:.3f} "
            f"executions={report.executions}"
        )

    print()
    print("SUMMARY")
    print("-" * 76)

    recovered = outcomes["RECOVERED"]
    screening_miss = outcomes["SCREENING_MISS"]
    confirmation_miss = outcomes["CONFIRMATION_MISS"]

    print(f"Recovered          : {recovered}/{RUNS} ({recovered / RUNS:.2%})")

    print(f"Screening misses   : {screening_miss}/{RUNS} ({screening_miss / RUNS:.2%})")

    print(
        f"Confirmation misses: "
        f"{confirmation_miss}/{RUNS} "
        f"({confirmation_miss / RUNS:.2%})"
    )

    print(f"Mean executions    : {mean(executions):.1f}")


if __name__ == "__main__":
    main()
