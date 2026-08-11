# Berliant / SCIF v0.0.4 Paper Outline

## Working Title

Adaptive Discovery of Mixed-Order Stochastic Capability Interactions in AI Systems

## 1. Abstract

- Problem: combinatorial interaction failures are difficult to discover efficiently.
- Limitation of exhaustive enumeration.
- Limitation of pairwise-only discovery.
- Limitation of deletion-based localization under overlapping or mixed interactions.
- Proposed method: SCIF v0.0.4.
- Components:
  - adaptive pairwise screening
  - known-pair suppression
  - residual-risk detection
  - higher-order localization
- Main empirical results:
  - 6999/7000 exact holdout recovery
  - zero false interaction candidates
  - exact recovery on overlapping, triple, and mixed scenarios
  - 75.48% to 96.14% execution reduction in scaling experiments.

## 2. Introduction

### 2.1 Problem

Modern AI systems expose multiple interacting capabilities.

Failures may arise only when several capabilities are enabled together.

### 2.2 Challenge

For n capabilities, exhaustive interaction testing grows combinatorially.

Order-3 exhaustive configurations:

1 + n + C(n,2) + C(n,3)

### 2.3 Research Gap

Existing pairwise discovery cannot identify pure higher-order interactions.

Deletion localization can identify a dominant monotonic interaction,
but may fail when interactions overlap or when lower- and higher-order
faults coexist.

### 2.4 Contribution

1. BSIB benchmark family for stochastic capability interaction failures.
2. SCIF adaptive pairwise discovery.
3. Residual-risk detection after suppression of known interactions.
4. Residual higher-order localization.
5. Evaluation on null, pairwise, overlapping, pure higher-order,
   mixed-order, sensitivity, ablation, and scaling settings.

## 3. Background and Problem Formulation

### 3.1 Capability Configuration

Define configuration:

C subseteq K

where K is the set of available capabilities.

### 3.2 Failure Probability

Each configuration induces an unknown stochastic failure probability:

p(C) = P(Y = 1 | C)

### 3.3 Interaction Risk

An interaction exists when the joint configuration exhibits excess
failure probability beyond its relevant lower-order subsets.

### 3.4 Joint Risk Increment

Define a joint-risk increment relative to subsets.

### 3.5 Discovery Objective

Recover minimal interaction sets while minimizing simulator executions.

## 4. BSIB Benchmark

### 4.1 Simulator

- stochastic binary failure outcome
- hidden ground-truth probability
- deterministic keyed random streams
- order/interleaving invariant execution

### 4.2 Benchmark Scenarios

- NULL
- PAIR-001
- PAIR-002
- PAIR-003
- OVERLAP
- TRIPLE
- MIXED

### 4.3 Scaling Benchmarks

- 8 capabilities
- 12 capabilities
- 16 capabilities
- 20 capabilities

## 5. SCIF Method

### 5.1 SCIF V3 Pairwise Discovery

- initial screening
- borderline retesting
- balanced confirmation
- minimal subset comparison

### 5.2 Limitation of Pairwise Discovery

Pure higher-order interactions generate no pairwise signal.

### 5.3 Known-Pair Suppression

Construct removal sets that disable already-discovered pairwise
interactions.

### 5.4 Residual-Risk Detection

Probe configurations after known interactions are suppressed.

Escalate only when substantial unexplained failure risk remains.

### 5.5 Residual Higher-Order Localization

Apply deletion-style localization inside the residual configuration.

### 5.6 Minimality Confirmation

Confirm candidate interaction and immediate subsets.

### 5.7 Overall SCIF V4 Pipeline

Pairwise discovery
→ pair suppression
→ residual probe
→ conditional higher-order localization
→ unified report.

## 6. Experimental Setup

### 6.1 Baselines

- SCIF V3
- Deletion localization
- Exhaustive discovery
- SCIF V4

### 6.2 Metrics

- exact recovery
- false-positive runs
- residual classification accuracy
- simulator executions
- execution reduction
- wall-clock time

### 6.3 Holdout Evaluation

1000 unseen seeds per scenario.

Total:

7000 unseen runs.

### 6.4 Baseline Comparison

100 seeds per selected benchmark.

### 6.5 Ablation

- V3 pairwise only
- V3 + residual detection
- Full V4

### 6.6 Sensitivity

Parameters:

- initial_trials
- min_residual_increment
- higher_order_min_removal_drop

### 6.7 Scaling

Capability counts:

8, 12, 16, 20.

## 7. Results

### 7.1 Holdout Recovery

Primary table:
results/paper/holdout_results.csv

Primary observation:

6999 / 7000 exact recovery.

### 7.2 Rare Weak-Pair Miss

PAIR-002 seed 31269.

The initial 100-trial sample observed:

- pair rate = 0.10
- baseline rate = 0.10
- JRI = 0.00

The interaction therefore did not advance beyond initial screening.

No false higher-order interaction was produced.

### 7.3 Method Comparison

Primary table:
results/paper/method_comparison.csv

Key result:

MIXED:
- SCIF V3 = 0%
- Deletion = 0%
- Exhaustive = 100%
- SCIF V4 = 100%

### 7.4 Ablation

Residual detection is required to identify unexplained higher-order risk.

Localization is required to convert residual risk into an exact
higher-order candidate.

### 7.5 Sensitivity

Default:

higher_order_min_removal_drop = 0.10

Threshold 0.05 was too permissive and allowed stochastic removal noise
to admit irrelevant capabilities.

### 7.6 Scaling

Primary table:
results/paper/scaling_results.csv

Execution reduction:

- n=8: 75.48%
- n=12: 89.63%
- n=16: 94.15%
- n=20: 96.14%

## 8. Discussion

### 8.1 Why V4 Works on Mixed Interactions

Known-pair suppression separates already-explained risk from
unexplained residual risk.

### 8.2 Adaptive Cost

Higher-order localization is invoked only when residual evidence
justifies escalation.

### 8.3 Comparison with Exhaustive Discovery

Exhaustive discovery remains a strong oracle baseline but becomes
increasingly expensive as capability count grows.

### 8.4 Comparison with Deletion Localization

Deletion works well for one dominant pure interaction but may be masked
by overlapping or mixed-order interactions.

## 9. Limitations

1. Current higher-order localizer returns at most one residual
   higher-order candidate.
2. Evaluation currently focuses on interactions up to order three.
3. Current benchmark fault resolution uses the maximum active failure
   probability.
4. Minimal hitting-set enumeration may become computationally expensive
   for larger capability sets.
5. Scaling study currently uses 20 seeds per capability count.
6. Evaluation is synthetic and does not yet establish external validity
   on production AI systems.
7. Parameter sensitivity was evaluated over a limited range.

## 10. Threats to Validity

### 10.1 Internal Validity

Monte Carlo sampling variation.

### 10.2 Construct Validity

Synthetic probability models approximate rather than fully reproduce
real-world AI failure mechanisms.

### 10.3 External Validity

Results cannot yet be generalized directly to arbitrary production
systems.

### 10.4 Statistical Conclusion Validity

Holdout uses 1000 seeds per principal scenario, while some auxiliary
studies use fewer seeds.

## 11. Reproducibility

Repository components:

- benchmarks/
- src/
- experiments/
- results/
- results/paper/

Research milestone:

scif-v0.0.4

## 12. Conclusion

SCIF v0.0.4 combines adaptive pairwise discovery with conditional
higher-order escalation.

The evaluated system preserves strong pairwise recovery, detects pure
higher-order interactions, resolves the tested mixed-order setting,
and substantially reduces simulator executions relative to exhaustive
order-3 search.
