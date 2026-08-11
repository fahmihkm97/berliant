# SCIF v0.0.4 Experimental Summary

## Core capability

SCIF v0.0.4 combines:

1. SCIF v0.0.3 pairwise discovery
2. known-pair suppression
3. residual-risk detection
4. residual higher-order localization
5. unified mixed-order reporting

## 1000-seed unseen holdout

| Scenario | Exact Recovery | False Positive Runs | Mean Executions |
|---|---:|---:|---:|
| NULL | 1000/1000 (100.0%) | 0/1000 | 4,907.6 |
| PAIR-001 | 1000/1000 (100.0%) | 0/1000 | 10,800.0 |
| PAIR-002 | 999/1000 (99.9%) | 0/1000 | 10,946.2 |
| PAIR-003 | 1000/1000 (100.0%) | 0/1000 | 10,846.2 |
| OVERLAP | 1000/1000 (100.0%) | 0/1000 | 13,100.0 |
| TRIPLE | 1000/1000 (100.0%) | 0/1000 | 17,712.3 |
| MIXED | 1000/1000 (100.0%) | 0/1000 | 22,803.2 |

Overall exact recovery:
6999 / 7000 = 99.9857%

Observed false interaction candidates:
0

## PAIR-002 rare holdout miss

Seed: 31269

Observed initial screening:

- pair trials: 100
- pair failure rate: 0.100
- baseline failure rate: 0.100
- observed JRI: 0.000
- pair was not promoted beyond initial screening
- residual risk was detected
- no false higher-order candidate was produced

This is retained as an observed stochastic screening miss rather
than tuning the algorithm after inspecting holdout data.

## Baseline comparison — 100 seeds

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

## Ablation — 100 seeds

| Scenario | V3 only | V3 + Residual | Full V4 |
|---|---:|---:|---:|
| NULL | 100% | 100% | 100% |
| PAIR-002 | 100% | 100% | 100% |
| OVERLAP | 100% | 100% | 100% |
| TRIPLE | 0% | 100% escalation | 100% exact |
| MIXED | 0% | 100% escalation | 100% exact |

Across the ablation runs:

- false escalations: 0
- missed escalations: 0
- false higher-order candidates: 0

## Sensitivity

Frozen default parameters:

- initial_trials = 100
- min_residual_increment = 0.10
- higher_order_min_removal_drop = 0.10

The removal threshold 0.05 was too permissive:

- TRIPLE exact recovery: 95/100
- MIXED exact recovery: 96/100

The failures were caused by irrelevant capabilities occasionally
showing stochastic removal drops near 0.05-0.07 and entering an
oversized candidate. Minimality confirmation rejected those
candidates rather than producing false positives.

Removal threshold 0.10 and 0.15 both achieved 100% exact recovery
in this sensitivity experiment.

## Scaling

| Capabilities | Exact Recovery | Mean Executions | Exhaustive Order-3 | Reduction |
|---:|---:|---:|---:|---:|
| 8 | 20/20 (100%) | 22,800 | 93,000 | 75.48% |
| 12 | 20/20 (100%) | 31,000 | 299,000 | 89.63% |
| 16 | 20/20 (100%) | 40,800 | 697,000 | 94.15% |
| 20 | 20/20 (100%) | 52,200 | 1,351,000 | 96.14% |

Mean wall-clock time increased from approximately 0.23 seconds at
8 capabilities to 2.67 seconds at 20 capabilities.

The current minimal-hitting-set enumeration is therefore a
computational optimization target for larger capability sets,
even though simulator execution efficiency remains substantially
better than exhaustive order-3 discovery.

## Current conclusion

SCIF v0.0.4 preserves strong pairwise discovery while adding
adaptive higher-order escalation.

The evaluated prototype:

- handles single pairwise faults
- handles weak pairwise faults
- handles overlapping pairwise faults
- detects pure three-way interactions
- handles mixed pairwise + three-way interactions
- avoids higher-order escalation on null/pair-only scenarios
- substantially reduces simulator executions compared with
  exhaustive order-3 search
