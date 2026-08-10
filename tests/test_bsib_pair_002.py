from pathlib import Path

from berliant.bsib import Simulator, load_scenario

SCENARIO_PATH = Path("benchmarks/bsib_01/easy/BSIB-PAIR-002.yaml")


def estimate_failure_rate(
    simulator: Simulator,
    capabilities: set[str],
    trials: int = 10_000,
) -> float:
    failures = sum(not simulator.invoke(capabilities).success for _ in range(trials))

    return failures / trials


def test_weak_pairwise_interaction_is_present() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    tools_rate = estimate_failure_rate(
        Simulator(scenario, seed=101),
        {"tools"},
    )

    streaming_rate = estimate_failure_rate(
        Simulator(scenario, seed=102),
        {"streaming"},
    )

    joint_rate = estimate_failure_rate(
        Simulator(scenario, seed=103),
        {"tools", "streaming"},
    )

    assert 0.03 < tools_rate < 0.07
    assert 0.03 < streaming_rate < 0.07
    assert 0.21 < joint_rate < 0.27
