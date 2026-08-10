from pathlib import Path

from berliant.bsib import (
    KeyedSimulator,
    load_scenario,
)
from berliant.discovery import (
    DeletionLocalizationBaseline,
    ExhaustiveDiscovery,
    SCIFDiscoveryV3,
)

SCENARIO_PATH = Path("benchmarks/bsib_01/higher_order/BSIB-OVERLAP-001.yaml")

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


def estimate_failure_rate(
    simulator: KeyedSimulator,
    capabilities: set[str],
    trials: int = 10_000,
) -> float:
    failures = sum(not simulator.invoke(capabilities).success for _ in range(trials))

    return failures / trials


def test_overlap_ground_truth_is_present() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    fault_a_rate = estimate_failure_rate(
        KeyedSimulator(
            scenario,
            seed=10001,
        ),
        {
            "tools",
            "streaming",
        },
    )

    fault_b_rate = estimate_failure_rate(
        KeyedSimulator(
            scenario,
            seed=10002,
        ),
        {
            "streaming",
            "strict_schema",
        },
    )

    healthy_pair_rate = estimate_failure_rate(
        KeyedSimulator(
            scenario,
            seed=10003,
        ),
        {
            "tools",
            "strict_schema",
        },
    )

    assert 0.52 < fault_a_rate < 0.58
    assert 0.47 < fault_b_rate < 0.53
    assert 0.01 < healthy_pair_rate < 0.05


def test_deletion_baseline_exposes_overlap_limit() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    simulator = KeyedSimulator(
        scenario,
        seed=10010,
    )

    engine = DeletionLocalizationBaseline(
        invoke=simulator.invoke,
        capabilities=scenario.capabilities,
        trials_per_config=1000,
        min_failure=0.20,
        min_removal_drop=0.20,
    )

    report = engine.discover()

    # Removing streaming disables both faults.
    assert report.removal_rates["streaming"] < 0.10

    # Removing tools leaves the second fault active.
    assert report.removal_rates["tools"] > 0.40

    # Removing strict_schema leaves the first fault active.
    assert report.removal_rates["strict_schema"] > 0.45

    # Only the shared capability appears essential,
    # which is insufficient to form an interaction.
    assert report.candidate is None


def test_exhaustive_pairwise_finds_both_overlapping_faults() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    simulator = KeyedSimulator(
        scenario,
        seed=10020,
    )

    engine = ExhaustiveDiscovery(
        invoke=simulator.invoke,
        capabilities=scenario.capabilities,
        max_order=2,
        trials_per_config=1000,
        min_joint_failure=0.20,
        min_jri=0.15,
    )

    report = engine.discover()

    discovered = {candidate.capabilities for candidate in report.candidates}

    assert FAULT_A in discovered
    assert FAULT_B in discovered
    assert report.executions == 37_000


def test_scif_v3_finds_both_overlapping_faults() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    simulator = KeyedSimulator(
        scenario,
        seed=10030,
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
        seed=20260810 + 10030,
    )

    report = engine.discover()

    discovered = {candidate.capabilities for candidate in report.candidates}

    assert FAULT_A in discovered
    assert FAULT_B in discovered
    assert report.executions < 37_000
