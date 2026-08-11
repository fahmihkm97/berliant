from pathlib import Path

from berliant import (
    KeyedSimulator,
    load_scenario,
    validated_scif,
)

ROOT = Path(__file__).resolve().parents[1]

scenario = load_scenario(
    ROOT / "benchmarks/bsib_01/mixed/BSIB-MIXED-001.yaml"
)

simulator = KeyedSimulator(
    scenario=scenario,
    seed=42,
)

discovery = validated_scif(
    invoke=simulator.invoke,
    capabilities=scenario.capabilities,
)

report = discovery.discover()

print(f"Scenario: {scenario.id}")
print(f"Executions: {report.executions}")

print(
    "Pairwise interactions:",
    [
        candidate.capabilities
        for candidate in report.pairwise_report.candidates
    ],
)

if report.higher_order is not None:
    print(
        "Higher-order interaction:",
        report.higher_order.candidate,
    )
else:
    print("Higher-order interaction: none")
