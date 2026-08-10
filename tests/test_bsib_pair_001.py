from pathlib import Path

from berliant.bsib import Simulator, load_scenario

SCENARIO_PATH = Path("benchmarks/bsib_01/easy/BSIB-PAIR-001.yaml")


def estimate_failure_rate(
    simulator: Simulator,
    capabilities: set[str],
    trials: int = 5000,
) -> float:
    failures = 0

    for _ in range(trials):
        result = simulator.invoke(capabilities)

        if not result.success:
            failures += 1

    return failures / trials


def test_pairwise_interaction_is_present() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    tools_rate = estimate_failure_rate(
        Simulator(scenario, seed=1),
        {"tools"},
    )

    structured_rate = estimate_failure_rate(
        Simulator(scenario, seed=2),
        {"structured_output"},
    )

    joint_rate = estimate_failure_rate(
        Simulator(scenario, seed=3),
        {"tools", "structured_output"},
    )

    assert tools_rate < 0.05
    assert structured_rate < 0.05
    assert 0.65 < joint_rate < 0.75
