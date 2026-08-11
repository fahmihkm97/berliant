# Research Questions

This study evaluates whether residual-risk-guided escalation can recover stochastic mixed-order capability interactions accurately while reducing the cost of exhaustive higher-order discovery.

## RQ1 — Discovery Accuracy

**How accurately does SCIF v0.0.4 recover hidden interaction structures under stochastic outcomes?**

We evaluate exact recovery, missed interactions, and observed false interaction candidates across the unseen BSIB holdout.

## RQ2 — Efficiency Relative to Baselines

**How does SCIF v0.0.4 compare with pairwise discovery, deletion localization, and exhaustive discovery?**

We compare both exact interaction recovery and simulator execution cost on representative pairwise, overlapping, pure-three-way, and mixed-order scenarios.

## RQ3 — Contribution of Residual-Risk Reasoning

**Do residual-risk detection and higher-order localization provide distinct benefits?**

Ablation experiments compare pairwise discovery alone, pairwise discovery with residual-risk detection, and the complete SCIF V4 pipeline.

## RQ4 — Parameter Sensitivity

**How sensitive is recovery to key sampling and localization thresholds?**

We vary initial sampling, residual-risk, and removal thresholds while monitoring recovery and false interaction candidates.

## RQ5 — Scaling Behavior

**How does SCIF behave as capability count increases?**

We measure exact recovery, simulator executions, reduction relative to exhaustive order-three discovery, and wall-clock behavior from 8 to 20 capabilities.
