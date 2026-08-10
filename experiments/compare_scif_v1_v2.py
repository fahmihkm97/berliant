from statistics import mean

from berliant.bsib import Simulator, load_scenario
from berliant.discovery import (
    SCIFDiscovery,
    SCIFDiscoveryV2,
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


def evaluate_v1() -> tuple[int, int, float]:
    scenario = load_scenario(SCENARIO_PATH)

    recoveries = 0
    false_positive_runs = 0
    executions: list[int] = []

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


def main() -> None:
    v1_recovery, v1_fp, v1_exec = evaluate_v1()
    v2_recovery, v2_fp, v2_exec = evaluate_v2()

    v1_reduction = (1 - v1_exec / EXHAUSTIVE_EXECUTIONS) * 100

    v2_reduction = (1 - v2_exec / EXHAUSTIVE_EXECUTIONS) * 100

    print()
    print("SCIF V1 vs V2 — BSIB-PAIR-002")
    print("=" * 72)

    print()
    print("SCIF v0.0.1")
    print("-" * 72)
    print(f"Recovery            : {v1_recovery}/{RUNS} ({v1_recovery / RUNS:.2%})")
    print(f"False-positive runs : {v1_fp}/{RUNS} ({v1_fp / RUNS:.2%})")
    print(f"Mean executions     : {v1_exec:.1f}")
    print(f"Reduction exhaustive: {v1_reduction:.2f}%")

    print()
    print("SCIF v0.0.2")
    print("-" * 72)
    print(f"Recovery            : {v2_recovery}/{RUNS} ({v2_recovery / RUNS:.2%})")
    print(f"False-positive runs : {v2_fp}/{RUNS} ({v2_fp / RUNS:.2%})")
    print(f"Mean executions     : {v2_exec:.1f}")
    print(f"Reduction exhaustive: {v2_reduction:.2f}%")

    print()
    print("CHANGE V1 -> V2")
    print("-" * 72)

    recovery_change = v2_recovery - v1_recovery

    execution_change = ((v2_exec / v1_exec) - 1) * 100

    print(f"Recovery change     : {recovery_change:+d} percentage points")

    print(f"Execution change    : {execution_change:+.2f}%")


if __name__ == "__main__":
    main()
