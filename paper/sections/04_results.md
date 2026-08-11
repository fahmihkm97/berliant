# Results

## 1. RQ1 — Holdout Discovery Accuracy

SCIF v0.0.4 achieved near-perfect exact recovery across the unseen
1,000-seed holdout evaluation.

| Scenario | Exact Recovery | False-Positive Runs | Mean Executions |
|---|---:|---:|---:|
| NULL | 1000/1000 (100.0%) | 0/1000 | 4,907.6 |
| PAIR-001 | 1000/1000 (100.0%) | 0/1000 | 10,800.0 |
| PAIR-002 | 999/1000 (99.9%) | 0/1000 | 10,946.2 |
| PAIR-003 | 1000/1000 (100.0%) | 0/1000 | 10,846.2 |
| OVERLAP | 1000/1000 (100.0%) | 0/1000 | 13,100.0 |
| TRIPLE | 1000/1000 (100.0%) | 0/1000 | 17,712.3 |
| MIXED | 1000/1000 (100.0%) | 0/1000 | 22,803.2 |

Across all seven scenarios, SCIF v0.0.4 obtained

\[
6999 / 7000
=
99.9857\%
\]

exact recovery.

No false interaction candidate was observed in the 7,000 holdout runs.

The result indicates that the method preserved strong recovery across
null, pairwise, overlapping-pair, pure-triple, and mixed-order
settings.

## 2. Rare PAIR-002 Holdout Miss

The only exact-recovery miss occurred in `PAIR-002` at seed 31269.

During the initial 100-trial screening stage, the observations were:

- target-pair failures: 10/100;
- target-pair failure rate: 0.100;
- baseline failure rate: 0.100; and
- observed joint-risk increment: 0.000.

The true weak pair therefore appeared indistinguishable from baseline
in this particular initial stochastic sample and was not promoted for
additional pairwise evaluation.

The residual stage subsequently observed a residual failure rate of
0.242 and correctly recognized unexplained risk.

However, higher-order localization did not report a false interaction.

The final run therefore represented a false negative for the weak
pair, not a false interaction discovery.

The parameters were deliberately left unchanged after observing this
holdout failure.

## 3. RQ2 — Comparison with Discovery Baselines

The method-comparison experiment shows that no evaluated baseline
provided the same behavior across all four representative interaction
structures.

| Scenario | Method | Recovery | Mean Executions |
|---|---|---:|---:|
| PAIR-002 | SCIF V3 | 100% | 7,900 |
| PAIR-002 | Deletion | 2% | 9,570 |
| PAIR-002 | Exhaustive | 100% | 37,000 |
| PAIR-002 | SCIF V4 | 100% | 10,900 |
| OVERLAP | SCIF V3 | 100% | 10,100 |
| OVERLAP | Deletion | 0% | 9,000 |
| OVERLAP | Exhaustive | 100% | 37,000 |
| OVERLAP | SCIF V4 | 100% | 13,100 |
| TRIPLE | SCIF V3 | 0% | 3,700 |
| TRIPLE | Deletion | 100% | 13,000 |
| TRIPLE | Exhaustive | 100% | 93,000 |
| TRIPLE | SCIF V4 | 100% | 17,700 |
| MIXED | SCIF V3 | 0% | 7,800 |
| MIXED | Deletion | 0% | 9,000 |
| MIXED | Exhaustive | 100% | 93,000 |
| MIXED | SCIF V4 | 100% | 22,800 |

### Pairwise scenario

On PAIR-002, both SCIF V3 and V4 reached 100% recovery.

V3 required fewer executions because it terminates after pairwise
discovery, whereas V4 additionally performs residual-risk verification.

### Overlapping pairwise interactions

SCIF V3 and V4 both recovered the two overlapping pairs in every run.

Deletion localization failed because the benchmark does not contain a
single dominant interaction that can be isolated through the removal
criterion used by that baseline.

### Pure triple

Pairwise SCIF recovered none of the pure triple interactions because
the proper pairwise subsets remained near baseline.

Deletion recovered the isolated triple in all 100 runs.

SCIF V4 also achieved 100% exact recovery while requiring a mean of
17,700 executions compared with 93,000 for exhaustive order-three
discovery.

This corresponds to an execution reduction of approximately 80.97%.

### Mixed-order interaction

The MIXED benchmark produced the clearest architectural distinction.

SCIF V3 recovered the pairwise interaction but could not represent the
hidden triple, resulting in 0% exact recovery.

Deletion localization also produced 0% exact recovery because the
pairwise interaction masked removal evidence from the higher-order
fault.

Exhaustive discovery obtained 100% recovery at 93,000 executions.

SCIF V4 obtained the same exact recovery with 22,800 mean executions,
representing a reduction of approximately 75.48%.

## 4. RQ3 — Ablation of Residual-Risk Reasoning

The ablation experiment isolates the contribution of the two new
higher-order stages.

| Scenario | V3 Pairwise Only | V3 + Residual | Full V4 |
|---|---:|---:|---:|
| NULL | 100% | 100% | 100% |
| PAIR-002 | 100% | 100% | 100% |
| OVERLAP | 100% | 100% | 100% |
| TRIPLE | 0% | 100% correct escalation | 100% exact recovery |
| MIXED | 0% | 100% correct escalation | 100% exact recovery |

Across all 500 ablation runs:

- false residual escalations: 0;
- missed residual escalations: 0; and
- false higher-order candidates: 0.

The results separate two functions of the V4 extension.

First, residual-risk detection determines whether the currently
discovered interactions fully explain the observed risk.

Second, higher-order localization identifies the exact interaction
responsible for unexplained residual risk.

For TRIPLE, mean execution counts were:

- V3 only: 3,700;
- V3 + residual: 4,700; and
- full V4: 17,700.

For MIXED they were:

- V3 only: 7,800;
- V3 + residual: 10,800; and
- full V4: 22,800.

Higher-order localization therefore adds cost only when escalation is
required.

## 5. RQ4 — Parameter Sensitivity

The default configuration achieved 100% exact recovery on all four
sensitivity scenarios.

Changing the residual-risk increment from 0.10 to either 0.05 or 0.15
did not reduce exact recovery in this experiment.

Similarly, increasing the higher-order minimum removal drop from 0.10
to 0.15 retained 100% exact recovery.

The principal sensitivity appeared when the removal threshold was
reduced to 0.05.

Under this setting:

- TRIPLE exact recovery decreased to 95/100; and
- MIXED exact recovery decreased to 96/100.

Diagnostic analysis showed that non-essential capabilities sometimes
exhibited stochastic removal drops slightly above the permissive 0.05
threshold.

Observed examples included spurious drops in approximately the
0.05-0.075 range.

These capabilities entered oversized candidate sets.

The subsequent minimality checks rejected those candidates, producing
`None` rather than a false higher-order interaction.

Thus, the permissive threshold primarily increased false-negative
localization rather than false-positive reporting.

The frozen value of 0.10 was retained.

## 6. RQ5 — Scaling Behavior

SCIF v0.0.4 retained 100% exact recovery for every tested capability
count in the scaling experiment.

| Capabilities | Exact Recovery | Mean SCIF V4 Executions | Exhaustive Executions | Reduction |
|---:|---:|---:|---:|---:|
| 8 | 20/20 (100%) | 22,800 | 93,000 | 75.48% |
| 12 | 20/20 (100%) | 31,000 | 299,000 | 89.63% |
| 16 | 20/20 (100%) | 40,800 | 697,000 | 94.15% |
| 20 | 20/20 (100%) | 52,200 | 1,351,000 | 96.14% |

The execution advantage increased with the size of the capability
space.

From 8 to 20 capabilities, exhaustive order-three execution cost grew
from 93,000 to 1,351,000 executions.

Over the same range, SCIF v0.0.4 increased from 22,800 to 52,200 mean
executions.

The relative execution reduction consequently increased from 75.48%
at eight capabilities to 96.14% at twenty capabilities.

## 7. Wall-Clock Scaling

Mean runtime in the synthetic scaling experiment was:

- 0.2282 seconds at 8 capabilities;
- 0.3179 seconds at 12 capabilities;
- 0.5400 seconds at 16 capabilities; and
- 2.6731 seconds at 20 capabilities.

The increase between 16 and 20 capabilities is substantially larger
than the increase in simulator execution count alone.

This behavior is consistent with the current implementation's
enumeration of minimal hitting sets during pair suppression.

The result therefore identifies a computational optimization target
for larger capability spaces even though SCIF remains substantially
more execution-efficient than exhaustive discovery.

## 8. Summary of Findings

The experiments provide the following answers to the research
questions.

**RQ1:** SCIF v0.0.4 achieved 99.9857% exact recovery across 7,000
unseen holdout runs with no observed false interaction candidates.

**RQ2:** SCIF v0.0.4 matched exhaustive recovery in the representative
100-seed comparison while substantially reducing simulator executions.
Unlike V3 and deletion localization, it recovered the tested mixed
pairwise-plus-triple scenario.

**RQ3:** Residual-risk detection correctly identified when
higher-order escalation was necessary, while residual localization
converted that evidence into exact higher-order recovery.

**RQ4:** The frozen parameters were stable across the tested
sensitivity range. A removal threshold of 0.05 was shown to be too
permissive to stochastic removal noise.

**RQ5:** Exact recovery remained 100% from 8 through 20 capabilities,
while execution reduction relative to exhaustive order-three search
increased from 75.48% to 96.14%.
