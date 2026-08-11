# Experimental Setup

## Benchmark Scenarios

The primary evaluation uses seven BSIB scenarios.

### NULL

`BSIB-NULL-001` contains no hidden interaction.

It evaluates whether the method avoids reporting interactions when
all configurations remain near baseline stochastic risk.

### PAIR-001

`BSIB-PAIR-001` contains a strong pairwise interaction between:

- `tools`; and
- `structured_output`.

### PAIR-002

`BSIB-PAIR-002` contains a weaker pairwise interaction between:

- `tools`; and
- `streaming`.

This scenario is specifically useful for evaluating stochastic
screening robustness.

### PAIR-003

`BSIB-PAIR-003` contains an interaction between:

- `parallel_tools`; and
- `strict_schema`.

It serves as an additional unseen pairwise scenario.

### OVERLAP

`BSIB-OVERLAP-001` contains two pairwise interactions that share one
capability:

- `tools + streaming`; and
- `streaming + strict_schema`.

The scenario tests whether the discovery procedure can recover more
than one overlapping pair.

### TRIPLE

`BSIB-TRIPLE-001` contains the pure higher-order interaction:

- `tools + streaming + strict_schema`.

Its proper pairs remain near baseline.

The scenario therefore provides no pairwise interaction signal for the
hidden triple.

### MIXED

`BSIB-MIXED-001` contains both:

- pair: `tools + streaming`; and
- triple: `reasoning + strict_schema + multimodal`.

The benchmark is designed to expose masking behavior that affects
single-interaction deletion localization.

## Evaluation Metrics

The principal metric is exact recovery.

A run is counted as exactly recovered only when the complete set of
reported interactions equals the benchmark ground truth.

Additional measures include:

- pairwise recovery;
- higher-order recovery;
- residual-risk classification;
- false-positive runs;
- mean simulator executions;
- median simulator executions;
- minimum and maximum executions;
- 95th-percentile execution count;
- reduction relative to exhaustive discovery; and
- wall-clock time in the scaling experiment.

## Unseen Holdout Evaluation

The primary holdout evaluation uses 1,000 unseen seeds per benchmark
scenario.

The holdout seed range is:

\[
31001,\ldots,32000.
\]

Seven scenarios are evaluated, producing a total of

\[
7 \times 1000 = 7000
\]

SCIF v0.0.4 holdout runs.

Parameters were not modified after observing the holdout results.

This is important because one rare weak-pair miss was retained and
analyzed rather than being used to retune the algorithm.

## Baseline Comparison

Four discovery methods are compared:

1. SCIF v0.0.3;
2. deletion-based localization;
3. exhaustive discovery; and
4. SCIF v0.0.4.

The comparison study uses 100 seeds from:

\[
41001,\ldots,41100.
\]

The selected scenarios are:

- PAIR-002;
- OVERLAP;
- TRIPLE; and
- MIXED.

For pairwise scenarios, exhaustive discovery evaluates configurations
through order two.

For scenarios containing a triple, exhaustive discovery evaluates
configurations through order three.

With eight capabilities this corresponds to:

\[
1 + 8 + \binom{8}{2}
=
37
\]

configurations for exhaustive order-two discovery, or 37,000
simulator executions at 1,000 trials per configuration.

For exhaustive order-three discovery:

\[
1 + 8 + \binom{8}{2} + \binom{8}{3}
=
93
\]

configurations are evaluated, corresponding to 93,000 simulator
executions.

## Ablation Study

The ablation study uses 100 seeds:

\[
51001,\ldots,51100.
\]

Five representative scenarios are evaluated:

- NULL;
- PAIR-002;
- OVERLAP;
- TRIPLE; and
- MIXED.

Three algorithmic stages are compared:

### Stage A — V3 Pairwise Only

Only confirmed pairwise discoveries are considered.

### Stage B — V3 + Residual Detection

Pairwise discovery is followed by residual-risk classification.

This stage determines whether higher-order escalation is needed but
does not yet localize a higher-order interaction.

### Stage C — Full V4

The complete pipeline includes residual higher-order localization.

The ablation records:

- stage success;
- false residual escalations;
- missed escalations;
- false higher-order candidates; and
- mean execution cost.

## Sensitivity Study

The sensitivity study uses 100 seeds:

\[
61001,\ldots,61100.
\]

Four scenarios are tested:

- NULL;
- PAIR-002;
- TRIPLE; and
- MIXED.

The frozen baseline configuration is:

- `initial_trials = 100`;
- `min_residual_increment = 0.10`; and
- `higher_order_min_removal_drop = 0.10`.

The evaluated alternatives are:

- initial trials = 50;
- initial trials = 200;
- residual increment = 0.05;
- residual increment = 0.15;
- removal drop = 0.05; and
- removal drop = 0.15.

The purpose is robustness characterization rather than post-holdout
parameter optimization.

## Scaling Study

Scaling is evaluated using benchmark variants with:

- 8 capabilities;
- 12 capabilities;
- 16 capabilities; and
- 20 capabilities.

Each benchmark retains:

- one pairwise interaction; and
- one three-way interaction.

Additional capabilities are non-interacting noise capabilities.

Twenty seeds are evaluated for each size:

\[
71001,\ldots,71020.
\]

For \(n\) capabilities, exhaustive order-three discovery evaluates

\[
1+n+\binom{n}{2}+\binom{n}{3}
\]

configurations.

At 1,000 trials per configuration, exhaustive execution counts are:

- 93,000 for 8 capabilities;
- 299,000 for 12 capabilities;
- 697,000 for 16 capabilities; and
- 1,351,000 for 20 capabilities.

## Reproducibility

The implementation is maintained in the Berliant repository.

The frozen research milestone is identified by the Git tag:

`scif-v0.0.4`

The repository includes:

- benchmark definitions;
- simulator implementation;
- discovery algorithms;
- automated tests;
- experiment scripts;
- aggregated result files; and
- publication figure-generation scripts.

All Python development commands are executed through the project's
`uv` environment.
