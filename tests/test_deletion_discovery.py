from pathlib import Path

from berliant.bsib import (
    KeyedSimulator,
    load_scenario,
)
from berliant.discovery import (
    DeletionLocalizationBaseline,
)

SCENARIO_PATH = Path("benchmarks/bsib_01/higher_order/BSIB-TRIPLE-001.yaml")

EXPECTED = tuple(
    sorted(
        (
            "tools",
            "streaming",
            "strict_schema",
        )
    )
)


def test_deletion_baseline_localizes_hidden_triple() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    simulator = KeyedSimulator(
        scenario,
        seed=9001,
    )

    engine = DeletionLocalizationBaseline(
        invoke=simulator.invoke,
        capabilities=(scenario.capabilities),
        trials_per_config=1000,
        min_failure=0.20,
        min_removal_drop=0.20,
    )

    report = engine.discover()

    assert report.candidate == EXPECTED

    assert report.candidate_failure_rate is not None

    assert report.candidate_failure_rate > 0.50

    assert max(report.immediate_subset_rates.values()) < 0.10

    # Full set:
    # 1 configuration
    #
    # Leave-one-out:
    # 8 configurations
    #
    # Exact candidate:
    # 1 configuration
    #
    # Candidate immediate subsets:
    # 3 configurations
    #
    # Total:
    # 13 * 1000 = 13,000 executions.
    assert report.executions == 13_000
