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

START_SEED = 1001
END_SEED = 2000
RUNS = END_SEED - START_SEED + 1

EXHAUSTIVE_EXECUTIONS = 37_000


def run_v2(
    scenario,
    seed: int,
) -> tuple[bool, bool, int]:
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

    recovered = EXPECTED in discovered
    false_positive = bool(discovered.difference({EXPECTED}))

    return (
        recovered,
        false_positive,
        report.executions,
    )


def run_v3(
    scenario,
    seed: int,
) -> tuple[bool, bool, int]:
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

    recovered = EXPECTED in discovered
    false_positive = bool(discovered.difference({EXPECTED}))

    return (
        recovered,
        false_positive,
        report.executions,
    )


def main() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    v2_recovery = 0
    v3_recovery = 0

    v2_fp = 0
    v3_fp = 0

    v2_exec: list[int] = []
    v3_exec: list[int] = []

    both = 0
    v2_only = 0
    v3_only = 0
    neither = 0

    for seed in range(
        START_SEED,
        END_SEED + 1,
    ):
        (
            v2_found,
            v2_false_positive,
            v2_executions,
        ) = run_v2(
            scenario,
            seed,
        )

        (
            v3_found,
            v3_false_positive,
            v3_executions,
        ) = run_v3(
            scenario,
            seed,
        )

        v2_recovery += int(v2_found)
        v3_recovery += int(v3_found)

        v2_fp += int(v2_false_positive)
        v3_fp += int(v3_false_positive)

        v2_exec.append(v2_executions)
        v3_exec.append(v3_executions)

        if v2_found and v3_found:
            both += 1
        elif v2_found:
            v2_only += 1
        elif v3_found:
            v3_only += 1
        else:
            neither += 1

    v2_mean = mean(v2_exec)
    v3_mean = mean(v3_exec)

    print()
    print("SCIF HOLDOUT VALIDATION")
    print("=" * 72)

    print(f"Seeds               : {START_SEED}-{END_SEED}")

    print()
    print("SCIF v0.0.2")
    print("-" * 72)
    print(f"Recovery            : {v2_recovery}/{RUNS} ({v2_recovery / RUNS:.2%})")
    print(f"False-positive runs : {v2_fp}/{RUNS} ({v2_fp / RUNS:.2%})")
    print(f"Mean executions     : {v2_mean:.1f}")

    print()
    print("SCIF v0.0.3")
    print("-" * 72)
    print(f"Recovery            : {v3_recovery}/{RUNS} ({v3_recovery / RUNS:.2%})")
    print(f"False-positive runs : {v3_fp}/{RUNS} ({v3_fp / RUNS:.2%})")
    print(f"Mean executions     : {v3_mean:.1f}")

    print()
    print("PAIRED OUTCOMES")
    print("-" * 72)
    print(f"Both recovered      : {both}")
    print(f"V2 only             : {v2_only}")
    print(f"V3 only             : {v3_only}")
    print(f"Neither             : {neither}")

    print()
    print("EFFICIENCY")
    print("-" * 72)

    v3_reduction = (1 - v3_mean / EXHAUSTIVE_EXECUTIONS) * 100

    print(f"V3 reduction vs exhaustive: {v3_reduction:.2f}%")

    change = ((v3_mean / v2_mean) - 1) * 100

    print(f"V3 execution change vs V2 : {change:+.2f}%")


if __name__ == "__main__":
    main()
