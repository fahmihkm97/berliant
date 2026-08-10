from pathlib import Path

from berliant.bsib import (
    KeyedSimulator,
    load_scenario,
)

SCENARIO_PATH = Path("benchmarks/bsib_01/easy/BSIB-PAIR-002.yaml")


def test_keyed_stream_is_interleaving_invariant() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    direct = KeyedSimulator(
        scenario,
        seed=777,
    )

    direct_tools = [direct.invoke({"tools"}).success for _ in range(100)]

    interleaved = KeyedSimulator(
        scenario,
        seed=777,
    )

    interleaved_tools: list[bool] = []

    for _ in range(100):
        tool_result = interleaved.invoke({"tools"})

        interleaved_tools.append(tool_result.success)

        interleaved.invoke({"streaming"})

        interleaved.invoke(
            {
                "tools",
                "streaming",
            }
        )

    assert direct_tools == interleaved_tools


def test_execution_result_hides_true_probability() -> None:
    scenario = load_scenario(SCENARIO_PATH)

    simulator = KeyedSimulator(
        scenario,
        seed=123,
    )

    result = simulator.invoke(
        {
            "tools",
            "streaming",
        }
    )

    assert not hasattr(
        result,
        "failure_probability",
    )
