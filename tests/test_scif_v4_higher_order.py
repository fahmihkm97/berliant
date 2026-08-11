from pathlib import Path

import pytest

from berliant.bsib import (
    KeyedSimulator,
    load_scenario,
)
from berliant.discovery import SCIFDiscoveryV4

PURE_TRIPLE = tuple(
    sorted(
        (
            "tools",
            "streaming",
            "strict_schema",
        )
    )
)

MIXED_TRIPLE = tuple(
    sorted(
        (
            "reasoning",
            "strict_schema",
            "multimodal",
        )
    )
)


CASES = (
    (
        Path("benchmarks/bsib_01/higher_order/BSIB-TRIPLE-001.yaml"),
        PURE_TRIPLE,
    ),
    (
        Path("benchmarks/bsib_01/mixed/BSIB-MIXED-001.yaml"),
        MIXED_TRIPLE,
    ),
)


@pytest.mark.parametrize(
    (
        "scenario_path",
        "expected_triple",
    ),
    CASES,
)
def test_scif_v4_integrates_higher_order_localization(
    scenario_path: Path,
    expected_triple: tuple[str, ...],
) -> None:
    scenario = load_scenario(scenario_path)

    simulator = KeyedSimulator(
        scenario,
        seed=19001,
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
        higher_order_trials=1000,
        higher_order_min_failure=0.15,
        higher_order_min_removal_drop=0.10,
        higher_order_min_candidate_size=3,
        seed=20260810 + 19001,
    )

    report = engine.discover()

    assert report.residual.residual_detected

    assert report.higher_order is not None

    assert report.higher_order.candidate == expected_triple

    assert report.executions < 93_000
