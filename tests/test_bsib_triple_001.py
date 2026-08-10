from pathlib import Path

from berliant.bsib import (
    KeyedSimulator,
    load_scenario,
)
from berliant.discovery import (
    ExhaustiveDiscovery,
    SCIFDiscoveryV3,
)

SCENARIO_PATH = Path("benchmarks/bsib_01/higher_order/BSIB-TRIPLE-001.yaml")

EXPECTED = tuple(
    sorted(
        (
            "tools",
            "streaming",
            "strict_schema",
        )
    )
)


def estimate_failure_rate(
    simulator: KeyedSimulator,
    capabilities: set[str],
    trials: int = 10_000,
) -> float:
    failures = sum(not simulator.invoke(capabilities).success for _ in range(trials))

    return failures / trials


def test_triple_fault_has_no_pairwise_signal() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    pair_configs = [
        {"tools", "streaming"},
        {"tools", "strict_schema"},
        {"streaming", "strict_schema"},
    ]

    for index, config in enumerate(
        pair_configs,
        start=1,
    ):
        rate = estimate_failure_rate(
            KeyedSimulator(
                scenario,
                seed=8000 + index,
            ),
            config,
        )

        assert 0.01 < rate < 0.05

    triple_rate = estimate_failure_rate(
        KeyedSimulator(
            scenario,
            seed=8010,
        ),
        {
            "tools",
            "streaming",
            "strict_schema",
        },
    )

    assert 0.57 < triple_rate < 0.63


def test_scif_v3_exposes_pairwise_architecture_limit() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    simulator = KeyedSimulator(
        scenario,
        seed=8020,
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
        seed=20260810 + 8020,
    )

    report = engine.discover()

    assert report.candidates == ()


def test_order_three_exhaustive_finds_hidden_triple() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    simulator = KeyedSimulator(
        scenario,
        seed=8030,
    )

    engine = ExhaustiveDiscovery(
        invoke=simulator.invoke,
        capabilities=scenario.capabilities,
        max_order=3,
        trials_per_config=1000,
        min_joint_failure=0.20,
        min_jri=0.15,
    )

    report = engine.discover()

    assert report.candidates

    best = report.candidates[0]

    assert best.capabilities == EXPECTED
    assert best.joint_failure_rate > 0.50
    assert best.joint_risk_increment > 0.40

    # 1 empty + 8 singles + 28 pairs + 56 triples.
    assert report.executions == 93_000
