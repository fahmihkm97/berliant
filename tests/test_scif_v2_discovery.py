from pathlib import Path

from berliant.bsib import Simulator, load_scenario
from berliant.discovery import SCIFDiscoveryV2

SCENARIO_PATH = Path("benchmarks/bsib_01/easy/BSIB-PAIR-001.yaml")


def test_scif_v2_finds_hidden_pair_with_balanced_confirmation() -> None:
    scenario = load_scenario(SCENARIO_PATH)
    simulator = Simulator(
        scenario,
        seed=12345,
    )

    engine = SCIFDiscoveryV2(
        invoke=simulator.invoke,
        capabilities=scenario.capabilities,
        initial_trials=100,
        confirm_trials=1500,
        subset_confirm_trials=1000,
        min_joint_failure=0.20,
        min_jri=0.15,
        confidence_threshold=0.95,
        seed=20260810,
    )

    report = engine.discover()

    expected = tuple(
        sorted(
            (
                "tools",
                "structured_output",
            )
        )
    )

    assert report.candidates

    best = report.candidates[0]

    assert best.capabilities == expected
    assert best.joint_failure_rate > 0.60
    assert best.joint_risk_increment > 0.50
    assert best.confidence > 0.95

    # V2 must re-estimate relevant subsets during confirmation.
    assert report.stats[()].trials == 1000
    assert report.stats[("tools",)].trials == 1000
    assert report.stats[("structured_output",)].trials == 1000

    # Suspicious joint pair receives the larger confirmation budget.
    assert report.stats[expected].trials == 1500

    # It must still remain cheaper than the exhaustive baseline.
    assert report.executions < 37_000
