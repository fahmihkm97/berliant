from pathlib import Path

import pytest

from berliant.bsib import (
    KeyedSimulator,
    load_scenario,
)
from berliant.discovery import SCIFDiscoveryV4

CASES = (
    (
        Path("benchmarks/bsib_01/null/BSIB-NULL-001.yaml"),
        False,
        False,
    ),
    (
        Path("benchmarks/bsib_01/easy/BSIB-PAIR-001.yaml"),
        True,
        False,
    ),
    (
        Path("benchmarks/bsib_01/higher_order/BSIB-TRIPLE-001.yaml"),
        False,
        True,
    ),
    (
        Path("benchmarks/bsib_01/mixed/BSIB-MIXED-001.yaml"),
        True,
        True,
    ),
    (
        Path("benchmarks/bsib_01/higher_order/BSIB-OVERLAP-001.yaml"),
        True,
        False,
    ),
)


@pytest.mark.parametrize(
    (
        "scenario_path",
        "expect_pair",
        "expect_residual",
    ),
    CASES,
)
def test_scif_v4_residual_risk_detection(
    scenario_path: Path,
    expect_pair: bool,
    expect_residual: bool,
) -> None:
    scenario = load_scenario(scenario_path)

    simulator = KeyedSimulator(
        scenario,
        seed=15001,
    )

    engine = SCIFDiscoveryV4(
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
        residual_trials=1000,
        min_residual_failure=0.15,
        min_residual_increment=0.10,
        seed=20260810 + 15001,
    )

    report = engine.discover()

    has_pair = bool(report.pairwise_report.candidates)

    assert has_pair is expect_pair

    assert report.residual.residual_detected is expect_residual

    assert report.executions < 93_000
