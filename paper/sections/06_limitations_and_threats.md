# Limitations and Threats to Validity

## 1. Synthetic and External Validity

The evaluation uses synthetic BSIB benchmarks, which provide exact hidden ground truth and controlled failure probabilities but cannot reproduce the full complexity of production AI systems. Real systems may exhibit state dependence, non-stationarity, continuous parameters, semantic failures, environmental effects, and different interaction-composition rules.

The current results therefore establish behavior within the evaluated synthetic setting rather than universal production validity. External validation on real capability-rich systems remains necessary.

## 2. Interaction Scope

The experiments focus on pairwise and three-way interactions. Although SCIF v0.0.4 conditionally invokes higher-order localization, the present evaluation does not establish performance for arbitrary interaction orders.

The residual localizer also returns at most one higher-order candidate from a selected residual configuration. This is sufficient for the evaluated TRIPLE and MIXED scenarios but does not solve the general case of multiple simultaneous or overlapping higher-order interactions.

## 3. Hitting-Set Scalability

Known pairwise interactions are suppressed using minimal hitting sets. The current implementation directly enumerates candidate removal subsets.

This remained practical for the evaluated capability counts, but wall-clock growth at twenty capabilities indicates increasing computational overhead. More efficient hitting-set algorithms or optimization formulations may be required for substantially larger systems.

## 4. Benchmark Fault Composition

When several benchmark faults are active simultaneously, BSIB uses the maximum active failure probability. This is a deliberate modeling assumption.

Real systems may instead exhibit additive, multiplicative, conditional, or non-monotonic composition. SCIF should therefore be evaluated under additional fault-composition models before broader conclusions are drawn.

## 5. Stochastic Sampling and Parameters

The PAIR-002 holdout miss demonstrates that finite stochastic samples can occasionally obscure a real interaction. At seed 31269, the weak target pair and baseline produced the same empirical failure rate during initial screening, preventing the pair from being promoted.

Increasing sampling could reduce some false-negative risk but would increase execution cost. The frozen parameters therefore represent an empirical trade-off rather than a guarantee of perfect recovery.

Sensitivity analysis also explored only a limited parameter range. Weaker effects or different benchmark distributions may produce different operating points.

## 6. Scaling and Statistical Uncertainty

The main holdout uses 1,000 seeds per scenario, whereas the scaling study uses only twenty seeds per capability count. Scaling results therefore provide stronger evidence about execution trends than about precise recovery probabilities.

In particular, observed 20/20 recovery should not be interpreted as a zero underlying failure probability. Recovery proportions are reported with confidence intervals where appropriate.

## 7. Baselines and Construct Validity

The empirical comparison includes SCIF V3, deletion localization, exhaustive discovery, and SCIF V4. These baselines isolate the architectural questions studied here, but they do not constitute an exhaustive implementation-level comparison with the broader combinatorial-testing and probabilistic fault-localization literature.

Exact interaction recovery is appropriate for BSIB because the benchmark exposes known minimal interaction sets. Real debugging usefulness may additionally depend on severity, diagnosis latency, reproducibility, and explanation quality, which are not measured here.

## 8. Internal Validity

Keyed deterministic random streams reduce confounding caused by evaluation order, and the repository contains automated tests covering benchmark ground truth, simulator invariance, pairwise discovery, deletion localization, residual-risk detection, and higher-order localization.

All 34 automated tests pass at the frozen research milestone, but implementation errors remain a possible source of internal-validity risk.
