from pathlib import Path

import pytest

from berliant.bsib import (
    KeyedSimulator,
    load_scenario,
)
from berliant.discovery import (
    ResidualHigherOrderLocalizer,
    SCIFDiscoveryV4,
)

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
def test_residual_localizer_finds_hidden_triple(
    scenario_path: Path,
    expected_triple: tuple[str, ...],
) -> None:
    scenario = load_scenario(scenario_path)

    simulator = KeyedSimulator(
        scenario,
        seed=17001,
    )

    detector = SCIFDiscoveryV4(
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
        seed=20260810 + 17001,
    )

    detector_report = detector.discover()

    assert detector_report.residual.residual_detected

    probe_rates = detector_report.residual.probe_failure_rates

    removal_set = max(
        probe_rates,
        key=probe_rates.get,
    )

    removed = frozenset(removal_set)

    residual_configuration = tuple(
        capability for capability in scenario.capabilities if capability not in removed
    )

    localizer = ResidualHigherOrderLocalizer(
        invoke=simulator.invoke,
        trials_per_config=1000,
        min_failure=0.15,
        min_removal_drop=0.10,
        min_candidate_size=3,
    )

    localization = localizer.localize(residual_configuration)

    assert localization.candidate == expected_triple

    assert localization.candidate_failure_rate is not None

    assert localization.candidate_failure_rate > 0.50

    assert localization.executions < 20_000

    combined_executions = detector_report.executions + localization.executions

    assert combined_executions < 93_000
