# Research Questions

This study investigates whether stochastic interactions among AI-system
capabilities can be discovered accurately without exhaustively testing
all low-order capability combinations.

The evaluation is organized around the following research questions.

## RQ1 — Discovery Accuracy

**RQ1: How accurately does SCIF v0.0.4 recover stochastic capability
interactions across null, pairwise, overlapping, pure higher-order,
and mixed-order benchmark scenarios?**

This question evaluates exact interaction recovery rather than only
detecting whether a configuration is risky.

The evaluated scenario classes include:

- no hidden interaction;
- a strong pairwise interaction;
- a weak pairwise interaction;
- an unseen pairwise interaction;
- overlapping pairwise interactions;
- a pure three-way interaction; and
- a mixed pairwise plus three-way interaction.

Primary measures are exact recovery rate and false interaction
candidates.

## RQ2 — Efficiency Relative to Baselines

**RQ2: How does SCIF v0.0.4 compare with pairwise SCIF, deletion-based
localization, and exhaustive discovery in terms of recovery accuracy
and simulator executions?**

The purpose is to determine whether SCIF v0.0.4 can preserve the
recovery capability of exhaustive search while reducing the number of
required stochastic executions.

The comparison includes:

- SCIF v0.0.3;
- deletion-based localization;
- exhaustive discovery; and
- SCIF v0.0.4.

## RQ3 — Contribution of Residual-Risk Reasoning

**RQ3: What contribution do residual-risk detection and residual
higher-order localization make to mixed-order interaction discovery?**

An ablation study evaluates three progressively richer stages:

1. pairwise discovery only;
2. pairwise discovery plus residual-risk detection; and
3. the complete SCIF v0.0.4 pipeline.

This question tests whether residual-risk detection is necessary to
recognize unexplained higher-order risk and whether localization is
necessary to convert that residual evidence into an exact interaction
candidate.

## RQ4 — Parameter Robustness

**RQ4: How sensitive is SCIF v0.0.4 to reasonable variation in its
screening, residual-risk, and higher-order localization parameters?**

The sensitivity study varies:

- the number of initial pairwise trials;
- the minimum residual-risk increment; and
- the minimum removal drop used during higher-order localization.

The goal is not to optimize parameters after holdout evaluation, but
to characterize the stability of the frozen algorithm.

## RQ5 — Scaling Behavior

**RQ5: How does the execution cost of SCIF v0.0.4 scale as the number
of available capabilities increases?**

The scaling study evaluates systems containing:

- 8 capabilities;
- 12 capabilities;
- 16 capabilities; and
- 20 capabilities.

The principal comparison is between SCIF v0.0.4 execution cost and
the number of simulator executions required by exhaustive order-three
discovery.
