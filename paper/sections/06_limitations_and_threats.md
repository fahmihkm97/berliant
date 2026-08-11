# Limitations and Threats to Validity

## 1. Synthetic Evaluation

The present evaluation is based on synthetic BSIB benchmarks.

Synthetic benchmarks provide exact hidden ground truth and controlled
failure probabilities, making them useful for measuring discovery
accuracy.

However, they cannot reproduce the full complexity of failures in
production AI systems.

Real systems may contain state dependence, non-stationary behavior,
continuous parameters, semantic failures, environmental effects, and
interactions that do not follow the benchmark probability model.

The current results therefore establish behavior within the evaluated
synthetic setting rather than universal production validity.

## 2. Interaction Order

The present experiments focus primarily on pairwise and three-way
interactions.

SCIF v0.0.4 provides a mechanism for conditional higher-order
localization, but the evaluation does not establish performance for
arbitrary interaction orders.

As interaction size increases, both statistical requirements and
search complexity may change substantially.

## 3. Single Residual Higher-Order Candidate

The current residual localizer returns at most one higher-order
candidate from the selected residual configuration.

This is sufficient for the evaluated TRIPLE and MIXED benchmarks but
does not solve the general case of multiple simultaneous or
overlapping higher-order interactions.

Future versions should support iterative residual explanation or
multiple higher-order candidate extraction.

## 4. Minimal Hitting-Set Enumeration

Known pairwise interactions are suppressed using minimal hitting sets.

The current implementation enumerates candidate removal subsets
directly.

Although this was practical for the evaluated capability counts, the
wall-clock scaling experiment indicates increasing computational
overhead by twenty capabilities.

More efficient hitting-set algorithms or optimization formulations may
be needed for substantially larger systems.

## 5. Benchmark Fault Composition

When multiple benchmark faults are simultaneously active, the current
simulator resolves their effect using the maximum active failure
probability.

This is a deliberate benchmark assumption.

Other systems may exhibit additive, multiplicative, conditional, or
otherwise non-monotonic interaction composition.

The effect of different fault-composition rules requires separate
evaluation.

## 6. Stochastic False Negatives

The PAIR-002 holdout miss demonstrates that finite stochastic
screening can occasionally hide a real interaction.

At seed 31269, the target weak pair and baseline both produced an
observed failure rate of 0.10 during initial sampling.

Thus, even when the underlying interaction probability is elevated,
finite samples can produce insufficient empirical evidence.

Increasing initial sampling would reduce some of this risk but would
also increase execution cost.

The current parameters therefore represent a trade-off rather than a
guarantee of perfect recovery.

## 7. Parameter Range

Sensitivity analysis varied several important parameters but covered
only a limited range.

The experiment should not be interpreted as a complete parameter-space
analysis.

Other benchmark distributions or weaker interaction effects may
produce different optimal operating points.

## 8. Scaling Sample Size

The principal unseen holdout uses 1,000 seeds per scenario.

In contrast, the scaling study uses only twenty seeds per capability
count.

The scaling results therefore provide evidence about execution trends
and initial robustness, but the recovery estimates have substantially
wider uncertainty than the main holdout evaluation.

## 9. Baseline Scope

The current comparison includes:

- SCIF v0.0.3;
- deletion localization;
- exhaustive discovery; and
- SCIF v0.0.4.

These baselines are directly relevant to the architectural questions
studied in this work.

However, the study does not yet compare against the broader literature
on combinatorial interaction testing, adaptive experimentation,
statistical fault localization, group testing, or Bayesian search.

A broader related-work comparison is required before publication.

## 10. Internal Validity

Deterministic keyed random streams are used to reduce confounding from
evaluation order.

Nevertheless, implementation errors remain a possible source of
internal-validity risk.

The repository therefore includes automated tests for benchmark
ground truth, simulator invariance, pairwise discovery, deletion
localization, residual-risk detection, and higher-order localization.

At the frozen milestone, all 34 automated tests pass.

## 11. Construct Validity

Exact interaction recovery is a strict and interpretable metric because
the synthetic benchmark provides known minimal interaction sets.

However, real debugging usefulness may involve additional factors such
as severity, reproducibility, diagnosis latency, or the ability to
generate actionable explanations.

These dimensions are not measured in the current evaluation.

## 12. External Validity

The results cannot yet be generalized directly to arbitrary AI
platforms, model providers, agent frameworks, or real production
failures.

External validation will require execution against real capability
systems where interaction bugs occur naturally or can be independently
verified.

## 13. Statistical Conclusion Validity

The main holdout contains 7,000 runs and therefore provides much
stronger empirical support than the auxiliary 100-seed and 20-seed
studies.

Reported recovery rates should always be interpreted together with
their experiment size.

In particular, 100% recovery in a twenty-seed scaling experiment does
not imply a zero underlying failure probability.
