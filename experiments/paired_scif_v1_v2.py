from scipy.stats import binomtest

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


def run_v1(
    scenario: object,
    seed: int,
) -> tuple[bool, int]:
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

    return (
        EXPECTED in discovered,
        report.executions,
    )


def run_v2(
    scenario: object,
    seed: int,
) -> tuple[bool, int]:
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

    return (
        EXPECTED in discovered,
        report.executions,
    )


def main() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    both_found = 0
    v1_only = 0
    v2_only = 0
    neither = 0

    v1_execution_total = 0
    v2_execution_total = 0

    print()
    print("PAIRED SCIF V1 vs V2")
    print("=" * 72)

    for seed in range(1, RUNS + 1):
        v1_found, v1_exec = run_v1(
            scenario,
            seed,
        )

        v2_found, v2_exec = run_v2(
            scenario,
            seed,
        )

        v1_execution_total += v1_exec
        v2_execution_total += v2_exec

        if v1_found and v2_found:
            both_found += 1
            transition = "BOTH"

        elif v1_found and not v2_found:
            v1_only += 1
            transition = "V1_ONLY"

        elif not v1_found and v2_found:
            v2_only += 1
            transition = "V2_ONLY"

        else:
            neither += 1
            transition = "NEITHER"

        print(
            f"seed={seed:03d} {transition:<8} v1_exec={v1_exec:<5} v2_exec={v2_exec:<5}"
        )

    discordant = v1_only + v2_only

    if discordant > 0:
        result = binomtest(
            k=v2_only,
            n=discordant,
            p=0.5,
            alternative="two-sided",
        )

        p_value = result.pvalue
    else:
        p_value = 1.0

    print()
    print("PAIRED SUMMARY")
    print("-" * 72)

    print(f"Both recovered : {both_found}")

    print(f"V1 only        : {v1_only}")

    print(f"V2 only        : {v2_only}")

    print(f"Neither        : {neither}")

    print()
    print(f"Discordant runs: {discordant}")

    print(f"Exact paired p : {p_value:.10g}")

    print()
    print(f"V1 mean exec   : {v1_execution_total / RUNS:.1f}")

    print(f"V2 mean exec   : {v2_execution_total / RUNS:.1f}")


if __name__ == "__main__":
    main()
