from pathlib import Path

from berliant.bsib import Simulator, load_scenario
from berliant.discovery import ExhaustiveDiscovery

SCENARIO_PATH = Path("benchmarks/bsib_01/easy/BSIB-PAIR-001.yaml")


def test_exhaustive_discovery_finds_hidden_pair() -> None:
    scenario = load_scenario(SCENARIO_PATH)
    simulator = Simulator(scenario, seed=12345)

    discovery = ExhaustiveDiscovery(
        invoke=simulator.invoke,
        capabilities=scenario.capabilities,
        max_order=2,
        trials_per_config=1000,
        min_joint_failure=0.20,
        min_jri=0.15,
    )

    report = discovery.discover()

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

    # Empty config + 8 singles + C(8,2)=28 pairs.
    assert report.executions == 37_000
