# Berliant / SCIF v0.0.4 Artifact

This artifact accompanies the research prototype:

**SCIF v0.0.4 — Residual-Risk-Guided Discovery of Stochastic Mixed-Order Capability Interactions**

## Contents

The repository contains:

### Source code

`src/berliant/`

- BSIB stochastic simulator
- keyed deterministic random streams
- exhaustive discovery
- deletion localization baseline
- SCIF V1–V4

### Benchmarks

`benchmarks/`

- null scenarios
- pairwise scenarios
- overlapping interactions
- pure higher-order interaction
- mixed pairwise + higher-order interaction
- scaling benchmarks

### Experiments

`experiments/`

- multiseed validation
- 1000-seed unseen holdout
- baseline comparison
- ablation study
- sensitivity analysis
- scaling study
- statistical audit
- paper figure generation
- manuscript generation

### Results

`results/`

- experimental summaries
- paper-ready CSV files
- confidence-interval results
- publication figures

### Paper

`paper/`

- manuscript
- individual sections
- bibliography
- claim audit
- venue strategy
- submission checklist

## Frozen Research Milestone

The algorithmic research milestone is:

    scif-v0.0.4

This Git tag freezes the SCIF v0.0.4 implementation before later
paper-writing and artifact-preparation commits.

## Requirements

- Python 3.12
- uv

Install the locked environment with:

    uv sync

## Quality Checks

Run:

    uv run ruff check .
    uv run mypy src
    uv run pytest -q

Expected test result:

    34 passed

## Primary Experiments

### 100-Seed SCIF V4 Validation

    uv run python experiments/scif_v4_multiseed.py

### 1000-Seed Unseen Holdout

    uv run python experiments/scif_v4_holdout_1000.py

The holdout evaluates seven scenarios with 1000 unseen seeds
per scenario, for a total of 7000 SCIF V4 runs.

### Method Comparison

    uv run python experiments/scif_v4_comparison.py

Compared methods:

- SCIF V3
- deletion localization
- exhaustive discovery
- SCIF V4

### Ablation Study

    uv run python experiments/scif_v4_ablation.py

Evaluated stages:

1. V3 pairwise only
2. V3 plus residual-risk detection
3. full V4

### Sensitivity Study

    uv run python experiments/scif_v4_sensitivity.py

### Scaling Study

    uv run python experiments/scif_v4_scaling.py

Evaluated capability counts:

- 8
- 12
- 16
- 20

### Statistical Audit

    uv run python experiments/statistical_audit.py

### Generate Paper Figures

    uv run python experiments/make_paper_figures.py

### Rebuild Manuscript

    uv run python experiments/build_manuscript.py

## Main Holdout Result

Across the seven benchmark scenarios:

- exact recoveries: 6999 / 7000
- empirical exact recovery: 99.9857%
- observed false interaction candidates: 0

The only observed exact-recovery miss occurred on weak pairwise
scenario `PAIR-002` at seed `31269`.

## Reproducibility

The simulator uses keyed deterministic random streams.

For a fixed:

- benchmark scenario
- capability configuration
- random seed

the stochastic outcome stream is invariant to evaluation order.

This allows discovery methods to be compared without introducing
different random streams merely because the methods evaluate
configurations in different orders.

## Important Limitations

The primary evaluation is synthetic.

The current artifact does not establish equivalent performance on
production AI systems.

SCIF v0.0.4 currently:

- focuses on the evaluated pairwise and order-three settings
- localizes at most one residual higher-order candidate
- uses direct minimal hitting-set enumeration
- assumes benchmark fault composition using the maximum active
  failure probability

See:

    paper/sections/06_limitations_and_threats.md

for the complete limitations discussion.
