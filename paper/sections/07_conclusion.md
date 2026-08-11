# Conclusion

This work investigated stochastic capability-interaction discovery
without requiring exhaustive higher-order enumeration. SCIF v0.0.4
combines adaptive pairwise discovery, known-interaction suppression,
residual-risk detection, and conditional higher-order localization.
Its central principle is to increase search complexity only when the
interactions already discovered fail to explain the remaining risk.

On the BSIB benchmark family, SCIF achieved 6,999 exact recoveries
across 7,000 unseen holdout runs, with no observed false interaction
candidates. The single miss occurred on the deliberately weak
PAIR-002 interaction when its initial stochastic sample was
indistinguishable from baseline.

The method comparison showed that SCIF V4 recovered the evaluated
pairwise, overlapping, pure-triple, and mixed-order structures, while
pairwise-only and direct-deletion approaches failed on specific
higher-order or overlapping cases. Ablation further showed that
residual-risk detection and higher-order localization provide distinct
functions. Execution savings relative to exhaustive order-three
discovery also increased with capability count, reaching 96.14% at
twenty capabilities in the scaling experiment.

These findings support residual-risk-guided escalation as a promising
strategy for stochastic interaction discovery, but the current evidence
remains synthetic and limited to the evaluated interaction structures.
Future work should examine multiple overlapping higher-order faults,
alternative fault-composition models, larger capability spaces, more
efficient hitting-set computation, broader baselines, and real-system
validation.

Within the evaluated setting, SCIF demonstrates that strong mixed-order
interaction recovery can be achieved without paying the full execution
cost of exhaustive combinatorial search.
