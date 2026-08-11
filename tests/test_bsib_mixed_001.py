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

SCENARIO_PATH = Path("benchmarks/bsib_01/mixed/BSIB-MIXED-001.yaml")

PAIR_FAULT = tuple(
    sorted(
        (
            "tools",
            "streaming",
        )
    )
)

TRIPLE_FAULT = tuple(
    sorted(
        (
            "reasoning",
            "strict_schema",
            "multimodal",
        )
    )
)


def test_mixed_scenario_contains_pair_and_triple() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    assert len(scenario.faults) == 2

    faults = {tuple(sorted(fault.capabilities)) for fault in scenario.faults}

    assert PAIR_FAULT in faults
    assert TRIPLE_FAULT in faults


def test_scif_v3_finds_pair_but_misses_pure_triple() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    simulator = KeyedSimulator(
        scenario,
        seed=12001,
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
        seed=20260810 + 12001,
    )

    report = engine.discover()

    discovered = {candidate.capabilities for candidate in report.candidates}

    assert PAIR_FAULT in discovered

    # Architectural limitation of SCIF V3:
    # pairwise discovery cannot directly recover
    # a pure three-way interaction.
    assert TRIPLE_FAULT not in discovered

    assert report.executions < 93_000


def test_deletion_baseline_is_masked_by_mixed_faults() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    simulator = KeyedSimulator(
        scenario,
        seed=12001,
    )

    engine = DeletionLocalizationBaseline(
        invoke=simulator.invoke,
        capabilities=scenario.capabilities,
        trials_per_config=1000,
        min_failure=0.20,
        min_removal_drop=0.20,
    )

    report = engine.discover()

    # Multiple faults mask the deletion signal.
    assert report.candidate is None

    assert report.full_failure_rate > 0.50

    assert report.executions == 9_000


def test_order_three_exhaustive_finds_both_faults() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    simulator = KeyedSimulator(
        scenario,
        seed=12001,
    )

    engine = ExhaustiveDiscovery(
        invoke=simulator.invoke,
        capabilities=scenario.capabilities,
        max_order=3,
        trials_per_config=1000,
        min_joint_failure=0.15,
        min_jri=0.10,
    )

    report = engine.discover()

    discovered = {candidate.capabilities for candidate in report.candidates}

    assert PAIR_FAULT in discovered
    assert TRIPLE_FAULT in discovered

    # 1 baseline + 8 singles + 28 pairs + 56 triples.
    assert len(report.rates) == 93
    assert report.executions == 93_000
