from statistics import mean

from berliant.bsib import Simulator, load_scenario
from berliant.discovery import (
    SCIFDiscoveryV2,
    SCIFDiscoveryV3,
)

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
EXHAUSTIVE_EXECUTIONS = 37_000


def evaluate_v2() -> tuple[int, int, float]:
    scenario = load_scenario(SCENARIO_PATH)

    recoveries = 0
    false_positive_runs = 0
    executions: list[int] = []

    for seed in range(1, RUNS + 1):
        simulator = Simulator(
            scenario,
            seed=seed,
        )

        engine = SCIFDiscoveryV2(
            invoke=simulator.invoke,
            capabilities=scenario.capabilities,
            initial_trials=100,
            confirm_trials=1500,
            subset_confirm_trials=1000,
            min_joint_failure=0.15,
            min_jri=0.10,
            confidence_threshold=0.95,
            seed=20260810 + seed,
        )

        report = engine.discover()

        discovered = {candidate.capabilities for candidate in report.candidates}

        if EXPECTED in discovered:
            recoveries += 1

        if discovered.difference({EXPECTED}):
            false_positive_runs += 1

        executions.append(report.executions)

    return (
        recoveries,
        false_positive_runs,
        mean(executions),
    )


def evaluate_v3() -> tuple[int, int, float]:
    scenario = load_scenario(SCENARIO_PATH)

    recoveries = 0
    false_positive_runs = 0
    executions: list[int] = []

    for seed in range(1, RUNS + 1):
        simulator = Simulator(
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

        discovered = {candidate.capabilities for candidate in report.candidates}

        if EXPECTED in discovered:
            recoveries += 1

        if discovered.difference({EXPECTED}):
            false_positive_runs += 1

        executions.append(report.executions)

    return (
        recoveries,
        false_positive_runs,
        mean(executions),
    )


def main() -> None:
    v2_recovery, v2_fp, v2_exec = evaluate_v2()
    v3_recovery, v3_fp, v3_exec = evaluate_v3()

    v2_reduction = (1 - v2_exec / EXHAUSTIVE_EXECUTIONS) * 100

    v3_reduction = (1 - v3_exec / EXHAUSTIVE_EXECUTIONS) * 100

    recovery_change = v3_recovery - v2_recovery

    execution_change = ((v3_exec / v2_exec) - 1) * 100

    print()
    print("SCIF V2 vs V3 — BSIB-PAIR-002")
    print("=" * 72)

    print()
    print("SCIF v0.0.2")
    print("-" * 72)
    print(f"Recovery            : {v2_recovery}/{RUNS} ({v2_recovery / RUNS:.2%})")
    print(f"False-positive runs : {v2_fp}/{RUNS} ({v2_fp / RUNS:.2%})")
    print(f"Mean executions     : {v2_exec:.1f}")
    print(f"Reduction exhaustive: {v2_reduction:.2f}%")

    print()
    print("SCIF v0.0.3")
    print("-" * 72)
    print(f"Recovery            : {v3_recovery}/{RUNS} ({v3_recovery / RUNS:.2%})")
    print(f"False-positive runs : {v3_fp}/{RUNS} ({v3_fp / RUNS:.2%})")
    print(f"Mean executions     : {v3_exec:.1f}")
    print(f"Reduction exhaustive: {v3_reduction:.2f}%")

    print()
    print("CHANGE V2 -> V3")
    print("-" * 72)
    print(f"Recovery change     : {recovery_change:+d} percentage points")
    print(f"Execution change    : {execution_change:+.2f}%")


if __name__ == "__main__":
    main()
