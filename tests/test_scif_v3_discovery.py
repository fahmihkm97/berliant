from pathlib import Path

import pytest

from berliant.bsib import Simulator, load_scenario
from berliant.discovery import SCIFDiscoveryV3

SCENARIO_PATH = Path("benchmarks/bsib_01/easy/BSIB-PAIR-002.yaml")

EXPECTED = tuple(
    sorted(
        (
            "tools",
            "streaming",
        )
    )
)


@pytest.mark.parametrize(
    "simulator_seed",
    [
        13,
        21,
    ],
)
def test_scif_v3_recovers_borderline_screening_fault(
    simulator_seed: int,
) -> None:
    scenario = load_scenario(SCENARIO_PATH)

    simulator = Simulator(
        scenario,
        seed=simulator_seed,
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
        seed=20260810 + simulator_seed,
    )

    report = engine.discover()

    discovered = {candidate.capabilities for candidate in report.candidates}

    assert EXPECTED in discovered

    assert report.stats[EXPECTED].trials == 1500

    assert report.executions < 37_000
