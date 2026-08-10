from pathlib import Path

from berliant.bsib import Simulator, load_scenario
from berliant.discovery import SCIFDiscovery

SCENARIO_PATH = Path("benchmarks/bsib_01/easy/BSIB-PAIR-001.yaml")


def test_scif_finds_hidden_pair_efficiently() -> None:
    scenario = load_scenario(SCENARIO_PATH)
    simulator = Simulator(scenario, seed=12345)

    engine = SCIFDiscovery(
        invoke=simulator.invoke,
        capabilities=scenario.capabilities,
        initial_trials=100,
        confirm_trials=1000,
        min_joint_failure=0.20,
        min_jri=0.15,
        confidence_threshold=0.95,
        seed=20260810,
    )

    report = engine.discover()

    assert report.candidates

    best = report.candidates[0]

    expected = tuple(
        sorted(
            (
                "tools",
                "structured_output",
            )
        )
    )

    assert best.capabilities == expected
    assert best.joint_failure_rate > 0.60
    assert best.joint_risk_increment > 0.50
    assert best.confidence > 0.95

    assert report.executions < 10_000
    assert report.executions < 37_000
