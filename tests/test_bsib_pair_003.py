from pathlib import Path

from berliant.bsib import (
    KeyedSimulator,
    load_scenario,
)
from berliant.discovery import SCIFDiscoveryV3

SCENARIO_PATH = Path("benchmarks/bsib_01/medium/BSIB-PAIR-003.yaml")

EXPECTED = tuple(
    sorted(
        (
            "parallel_tools",
            "strict_schema",
        )
    )
)


def estimate_failure_rate(
    simulator: KeyedSimulator,
    capabilities: set[str],
    trials: int = 10_000,
) -> float:
    failures = sum(not simulator.invoke(capabilities).success for _ in range(trials))

    return failures / trials


def test_pair_003_ground_truth_is_present() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    parallel_rate = estimate_failure_rate(
        KeyedSimulator(
            scenario,
            seed=5001,
        ),
        {"parallel_tools"},
    )

    strict_rate = estimate_failure_rate(
        KeyedSimulator(
            scenario,
            seed=5002,
        ),
        {"strict_schema"},
    )

    joint_rate = estimate_failure_rate(
        KeyedSimulator(
            scenario,
            seed=5003,
        ),
        {
            "parallel_tools",
            "strict_schema",
        },
    )

    assert 0.02 < parallel_rate < 0.06
    assert 0.02 < strict_rate < 0.06
    assert 0.32 < joint_rate < 0.38


def test_scif_v3_finds_unseen_pair_003() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    simulator = KeyedSimulator(
        scenario,
        seed=5004,
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
        seed=20260810 + 5004,
    )

    report = engine.discover()

    discovered = {candidate.capabilities for candidate in report.candidates}

    assert EXPECTED in discovered
    assert report.executions < 37_000
