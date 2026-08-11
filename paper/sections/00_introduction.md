# Introduction

Modern AI systems increasingly expose multiple capabilities within a
single execution environment, including tool use, structured outputs,
streaming, multimodal processing, parallel tool invocation, reasoning,
strict schema enforcement, and explicit tool selection.

These capabilities are often evaluated individually. However, system
failures may emerge only when particular capabilities are activated
together. Recent tool-augmented language-model benchmarks have
demonstrated failures associated with unavailable tools, multi-tool
settings, and silent tool errors
[@trevino2025failtalms; @sun2024toolsfail]. Such studies motivate
closer analysis of capability-rich AI systems, although they do not
attempt the stochastic interaction-localization problem studied here.

In this work, capability-interaction failures refer to failures whose
risk is associated not with one capability in isolation but with a
specific combination of capabilities.

The discovery problem is difficult for two reasons.

First, failures are stochastic. Repeated execution of the same
configuration may produce both successful and failing outcomes.
Discovery therefore requires statistical evidence rather than a
single deterministic observation.

Second, the number of possible capability combinations grows
combinatorially. For \(n\) capabilities, exhaustive testing through
interaction order three requires

\[
1+n+\binom{n}{2}+\binom{n}{3}
\]

distinct configurations before repeated stochastic trials are taken
into account.

For eight capabilities this corresponds to 93 configurations. At
1,000 stochastic executions per configuration, exhaustive order-three
evaluation requires 93,000 executions. At twenty capabilities, the
same procedure requires 1,351 configurations, or 1,351,000 executions.

This creates a tension between discovery completeness and evaluation
cost.

Pairwise methods provide one way to reduce this cost. They can
efficiently identify interactions whose signal appears in
two-capability configurations. However, they cannot recover a pure
higher-order interaction when all lower-order subsets remain near
baseline.

A different strategy is deletion-based localization. Starting from a
high-risk configuration, capabilities are removed one at a time and
the resulting decrease in failure probability is used to infer which
capabilities are essential to the fault.

This approach can localize an isolated monotonic higher-order
interaction. However, it can become unreliable when multiple
interactions overlap or when lower- and higher-order interactions are
simultaneously active. In such cases, removing one capability may
disable one fault while another remains active, masking the evidence
required for localization.

This work studies whether these limitations can be addressed without
returning to exhaustive combinatorial search.

We introduce SCIF v0.0.4, an adaptive stochastic interaction discovery
pipeline that combines pairwise discovery with conditional
higher-order escalation.

The central idea is to distinguish **explained risk** from
**unexplained residual risk**.

SCIF first discovers pairwise interactions. It then constructs
configurations in which those known pairwise interactions are
suppressed. If the remaining configuration returns to baseline risk,
the algorithm terminates. If substantial risk remains, the unexplained
signal triggers higher-order localization inside the residual
configuration.

This produces the pipeline:

**pairwise discovery** $ightarrow$ **known-pair suppression** $ightarrow$ **residual-risk detection** $ightarrow$ **conditional higher-order localization**.
The method is evaluated using the Benchmark for Stochastic Interaction
Bugs (BSIB), a synthetic benchmark family designed to provide hidden
ground-truth capability interactions while exposing only stochastic
execution outcomes to discovery algorithms.

The evaluation covers:

- null configurations with no hidden interaction;
- strong and weak pairwise interactions;
- overlapping pairwise interactions;
- a pure three-way interaction;
- a mixed pairwise plus three-way interaction;
- ablation of the residual-risk stages;
- parameter sensitivity; and
- scaling from eight to twenty capabilities.

Across a 7,000-run unseen holdout evaluation, SCIF v0.0.4 achieved
6,999 exact recoveries, corresponding to 99.9857% exact recovery, with
no observed false interaction candidates.

In the tested mixed-order benchmark, pairwise SCIF and deletion
localization both failed to recover the complete interaction set,
while SCIF v0.0.4 achieved 100% exact recovery in the 100-seed method
comparison.

Relative to exhaustive order-three discovery, SCIF v0.0.4 reduced
mean simulator executions by 75.48% in the eight-capability mixed
setting. In the scaling study, the reduction increased to 96.14% at
twenty capabilities while exact recovery remained 100% across the
twenty evaluated seeds.

Prior work already establishes combinatorial interaction testing,
minimal failure-causing schemas, adaptive interaction localization,
masking-aware multiple-fault methods, and probabilistic fault
localization [@kuhn2008beyond; @nie2011mfs; @zhang2011fic;
@yilmaz2014masking; @niu2020multiple; @nishiura2024frog].

SCIF is therefore not positioned as the first adaptive, higher-order,
masking-aware, or probabilistic localization method. The contribution
evaluated here is narrower: **residual stochastic risk is used as an
escalation signal**. Interactions already supported by the data are
suppressed, the remaining risk is estimated through repeated execution,
and higher-order localization is invoked only when substantial
unexplained risk remains.

The contributions of this work are:

1. the BSIB benchmark formulation for controlled stochastic
   capability-interaction evaluation;
2. the SCIF pipeline combining pairwise discovery, known-interaction
   suppression, residual-risk detection, and conditional higher-order
   localization;
3. unseen-holdout, baseline-comparison, ablation, and sensitivity
   evaluation of the frozen method; and
4. an initial scaling analysis of recovery and execution cost as
   capability count increases.
