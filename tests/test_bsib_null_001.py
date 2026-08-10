from pathlib import Path

from berliant.bsib import (
    KeyedSimulator,
    load_scenario,
)
from berliant.discovery import SCIFDiscoveryV3

SCENARIO_PATH = Path("benchmarks/bsib_01/null/BSIB-NULL-001.yaml")


def test_null_scenario_contains_no_faults() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    assert scenario.faults == ()


def test_scif_v3_reports_no_interaction_on_null_scenario() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    simulator = KeyedSimulator(
        scenario,
        seed=3001,
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
        seed=20260810 + 3001,
    )

    report = engine.discover()

    assert report.candidates == ()
    assert report.executions < 37_000
