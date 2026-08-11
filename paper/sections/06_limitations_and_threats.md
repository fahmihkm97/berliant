# Limitations and Threats to Validity

## Synthetic and External Validity

BSIB provides controlled stochastic behavior and exact hidden ground
truth but cannot reproduce the full complexity of production AI
systems, including state dependence, non-stationarity, continuous
parameters, semantic failures, and environmental effects. The results
therefore characterize behavior only within the evaluated synthetic
setting; real-system validation remains necessary.

## Interaction Scope

The experiments cover pairwise and three-way interactions. They do not
establish performance for arbitrary interaction orders. The residual
localizer also returns at most one higher-order candidate from a
selected residual configuration, leaving multiple simultaneous or
overlapping higher-order interactions for future study.

## Hitting-Set Scalability

Known interactions are suppressed through minimal hitting sets.
Although practical at the evaluated sizes, wall-clock growth indicates
increasing enumeration overhead. Larger systems may require optimized
hitting-set algorithms or alternative formulations.

## Benchmark Fault Composition

BSIB uses the maximum active failure probability when multiple faults
are present. Real systems may exhibit additive, multiplicative,
conditional, or non-monotonic composition, so alternative composition
models require separate evaluation.

## Stochastic Sampling and Parameters

Finite stochastic samples can obscure weak interactions, as illustrated
by the PAIR-002 holdout miss. Increasing sampling may reduce such
false-negative risk at additional execution cost. Sensitivity analysis
also covered only a limited parameter range, so different effect sizes
or benchmark distributions may require different operating points.

## Scaling and Statistical Uncertainty

The holdout used 1,000 seeds per scenario, whereas scaling used only
twenty seeds per capability count. Scaling results therefore provide
stronger evidence about execution trends than precise recovery
probabilities; observed 20/20 recovery should not be interpreted as
zero underlying failure probability.

## Baselines and Construct Validity

The comparison includes SCIF V3, deletion localization, exhaustive
discovery, and SCIF V4, but not every method from the broader
fault-localization literature. Exact interaction recovery is
appropriate for BSIB's known ground truth, while production debugging
may also depend on severity, latency, reproducibility, and explanation
quality.

## Internal Validity

Keyed deterministic random streams reduce evaluation-order
confounding, and 34 automated tests cover the principal benchmark and
discovery components. Nevertheless, implementation errors remain a
possible threat to internal validity.
