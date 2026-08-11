# Berliant

Berliant is a Python library for discovering stochastic failure-inducing capability interactions.

## Status

Berliant is currently an early-stage research-oriented Python library.

Current version: `0.1.0`

## Requirements

- Python 3.10 or newer
- `uv` is recommended for development

## Quickstart

Berliant exposes its primary API directly from the package root.

```python
from berliant import KeyedSimulator, load_scenario, validated_scif

scenario = load_scenario(
    "benchmarks/bsib_01/mixed/BSIB-MIXED-001.yaml"
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

print(report.executions)
print([
    candidate.capabilities
    for candidate in report.pairwise_report.candidates
])

if report.higher_order is not None:
    print(report.higher_order.candidate)
```

Run the included example:

```bash
uv run python examples/quickstart.py
```

## Public API

Primary imports:

```python
from berliant import (
    SCIF,
    KeyedSimulator,
    Scenario,
    load_scenario,
    validated_scif,
)
```

- `validated_scif(...)` uses the configuration evaluated in Berliant's benchmark experiments.
- `SCIF(...)` provides full parameter control.
- `KeyedSimulator` provides deterministic configuration-keyed stochastic simulation.
- `Scenario` and `load_scenario(...)` define and load benchmark scenarios.

## Discovery Report

`discover()` returns an `SCIFV4Report` containing:

- `pairwise_report`
- `residual`
- `higher_order`
- `executions`

## Development

```bash
uv run ruff check .
uv run mypy src
uv run pytest -q
```

## License

A license has not yet been selected for the first public release.
