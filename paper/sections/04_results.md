# Results

## RQ1 — Holdout Discovery Accuracy

SCIF v0.0.4 achieved 99.9857% exact recovery across the unseen
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

Across all seven scenarios, SCIF obtained

\[
6999 / 7000 = 99.9857\%
\]

exact recovery, with a 95% Wilson interval of approximately
99.9191%--99.9975%. For scenarios with 1000/1000 observed recovery,
the corresponding interval is approximately 99.6173%--100%;
observed perfect recovery is therefore not interpreted as zero
underlying failure probability.

No false interaction candidate was observed in the 7,000 holdout runs.

## Rare PAIR-002 Holdout Miss

The only exact-recovery miss occurred on `PAIR-002` at seed 31269.
During the initial 100-trial screen, both the target pair and baseline
produced 10 failures, yielding an observed joint-risk increment of
0.000. The weak pair was therefore not promoted.

The residual stage later observed a failure rate of 0.242 and detected
unexplained risk, but higher-order localization correctly declined to
report an unsupported interaction. The run was consequently a false
negative rather than a false-positive discovery. Parameters were not
changed after observing this holdout result.

## RQ2 — Comparison with Discovery Baselines

The 100-seed comparison shows that the evaluated methods differ
substantially across interaction structures.

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

V3 and V4 both recovered the tested pairwise and overlapping-pair
structures, although V4 incurred additional residual-verification
cost. V3 could not recover the pure triple because its proper pairwise
subsets remained near baseline. Deletion recovered the isolated
TRIPLE but failed on OVERLAP and MIXED.

SCIF V4 achieved 100% recovery on all four representative scenarios.
For TRIPLE it used 17,700 mean executions versus 93,000 for exhaustive
order-three discovery, a reduction of approximately 80.97%. For MIXED,
V4 used 22,800 executions versus 93,000, a reduction of 75.48%.

## RQ3 — Ablation of Residual-Risk Reasoning

The ablation isolates the roles of residual-risk detection and
higher-order localization.

| Scenario | V3 Pairwise Only | V3 + Residual | Full V4 |
|---|---:|---:|---:|
| NULL | 100% | 100% | 100% |
| PAIR-002 | 100% | 100% | 100% |
| OVERLAP | 100% | 100% | 100% |
| TRIPLE | 0% | 100% correct escalation | 100% exact recovery |
| MIXED | 0% | 100% correct escalation | 100% exact recovery |

Across 500 ablation runs, there were no false residual escalations,
missed residual escalations, or false higher-order candidates.
Residual detection therefore identifies when current discoveries leave
important risk unexplained, while localization converts that evidence
into an exact higher-order candidate.

Mean executions for TRIPLE were 3,700 for V3, 4,700 for V3 plus
residual detection, and 17,700 for full V4. For MIXED they were 7,800,
10,800, and 22,800, respectively. Higher-order localization thus adds
substantial cost only after escalation is triggered.

## RQ4 — Parameter Sensitivity

The frozen configuration achieved 100% exact recovery across all four
sensitivity scenarios. Changing the residual-risk increment from 0.10
to 0.05 or 0.15 did not reduce recovery, and increasing the
higher-order minimum removal drop from 0.10 to 0.15 also preserved
exact recovery.

The important degradation occurred when the removal threshold was
reduced to 0.05: TRIPLE recovery fell to 95/100 and MIXED to 96/100.
Non-essential capabilities sometimes exhibited stochastic removal
drops of approximately 0.05--0.075, entering oversized candidate sets
that were subsequently rejected by minimality checks. The permissive
threshold therefore increased false-negative localization rather than
false-positive reporting. The frozen value of 0.10 was retained.

## RQ5 — Scaling Behavior

SCIF obtained 20/20 exact recoveries for every tested capability count.
Because only twenty seeds were used per size, the 95% Wilson interval
for 20/20 recovery is approximately 83.89%--100%; these results are
therefore initial stability evidence rather than precise recovery estimates.

| Capabilities | Exact Recovery | Mean SCIF V4 Executions | Exhaustive Executions | Reduction |
|---:|---:|---:|---:|---:|
| 8 | 20/20 (100%) | 22,800 | 93,000 | 75.48% |
| 12 | 20/20 (100%) | 31,000 | 299,000 | 89.63% |
| 16 | 20/20 (100%) | 40,800 | 697,000 | 94.15% |
| 20 | 20/20 (100%) | 52,200 | 1,351,000 | 96.14% |

From 8 to 20 capabilities, exhaustive order-three cost grew from
93,000 to 1,351,000 executions, whereas SCIF increased from 22,800 to
52,200. The relative reduction consequently increased from 75.48% to
96.14%.

## Wall-Clock Scaling

Mean synthetic runtime increased from 0.2282 seconds at 8 capabilities
to 0.3179, 0.5400, and 2.6731 seconds at 12, 16, and 20 capabilities,
respectively. The sharper increase from 16 to 20 capabilities is
consistent with overhead from the current minimal hitting-set
enumeration. Thus, simulator-execution savings do not imply uniformly
low internal computational complexity.
