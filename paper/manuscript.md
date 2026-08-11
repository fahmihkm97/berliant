# Residual-Risk-Guided Discovery of Stochastic Mixed-Order Capability Interactions

**Berliant Research Prototype — SCIF v0.0.4**

---

# Abstract

Modern AI systems combine capabilities such as tool use, structured
outputs, streaming, reasoning, multimodal processing, and parallel
execution. Failures may arise only when specific capabilities are
activated together, creating stochastic interaction bugs that are
difficult to identify through isolated testing. Exhaustive
combinatorial evaluation can recover such interactions but grows
rapidly with the number of capabilities, while pairwise discovery
cannot represent pure higher-order faults.

We present SCIF v0.0.4, an adaptive discovery method for stochastic
mixed-order capability interactions. SCIF first performs pairwise
screening and confirmation, suppresses already-discovered pairwise
interactions, measures unexplained residual risk, and conditionally
invokes higher-order localization only when substantial residual risk
remains.

We evaluate the method using the Benchmark for Stochastic Interaction
Bugs (BSIB), including null, strong and weak pairwise, overlapping
pairwise, pure three-way, and mixed pairwise-plus-three-way scenarios.
Across 7,000 unseen holdout runs, SCIF v0.0.4 achieved 6,999 exact
recoveries (99.9857%) with no observed false interaction candidates.
In a 100-seed method comparison, SCIF v0.0.4 achieved 100% exact
recovery on all four representative scenarios, including a mixed-order
case in which pairwise SCIF and deletion localization both achieved 0%
exact recovery. For the eight-capability mixed benchmark, SCIF used
22,800 mean simulator executions compared with 93,000 for exhaustive
order-three discovery, a 75.48% reduction.

Ablation experiments show that residual-risk detection correctly
identifies when higher-order escalation is required, while residual
localization is necessary to recover the exact higher-order
interaction. In scaling experiments from eight to twenty capabilities,
SCIF achieved 20/20 exact recoveries at each tested capability count,
while execution reduction relative to exhaustive order-three search
increased from 75.48% to 96.14%. Because these scaling conditions used
twenty seeds each, they are interpreted primarily as evidence of
execution-cost trends and initial robustness.

These results indicate that residual-risk-guided escalation can
substantially reduce stochastic interaction-discovery cost while
retaining strong recovery across the evaluated mixed-order benchmark
structures.

---

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
1+n+{n \choose 2}+{n \choose 3}
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

\[
\text{pairwise discovery}
\rightarrow
\text{known-pair suppression}
\rightarrow
\text{residual-risk detection}
\rightarrow
\text{conditional higher-order localization}.
\]

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

Prior research has established the foundations of combinatorial
interaction testing and minimal failure-causing schemas
[@kuhn2008beyond; @nie2011survey; @nie2011mfs]. Adaptive approaches
have also been developed for characterizing failure-causing
interactions [@zhang2011fic], while feedback-driven and multiple-fault
methods explicitly address masking effects
[@yilmaz2014masking; @niu2020multiple]. Statistical and probabilistic
fault-localization approaches further demonstrate that uncertainty
over candidate interaction causes is not unique to the present work
[@wang2019pfs; @ji2023bayesflo; @nishiura2024frog].

Accordingly, SCIF is not positioned as the first adaptive,
higher-order, masking-aware, or probabilistic fault-localization
method. The narrower contribution evaluated here is the use of
**residual stochastic risk as an escalation signal**: interactions
already supported by the data are suppressed, the remaining
configuration is repeatedly executed, and higher-order localization is
invoked only when substantial unexplained risk remains.

The contributions of this work are therefore:

1. a formulation of stochastic capability-interaction discovery as a
   minimal-risk localization problem;
2. the BSIB benchmark family for controlled stochastic interaction
   evaluation;
3. an adaptive pairwise discovery foundation;
4. known-interaction suppression followed by residual-risk detection;
5. conditional residual higher-order localization;
6. empirical comparison against pairwise, deletion, and exhaustive
   baselines;
7. ablation and sensitivity analysis of the proposed stages; and
8. an initial scaling analysis of discovery cost as capability count
   increases.

---

# Related Work

## 1. Combinatorial Interaction Testing

Combinatorial testing (CT) addresses faults that arise from interactions
among multiple input parameters or configuration options. Rather than
enumerating every possible system configuration, t-way testing constructs
test suites that cover combinations up to a selected interaction strength
[@kuhn2008beyond; @nie2011survey].

This literature provides the conceptual foundation for the present work:
system behavior may depend on combinations of capabilities rather than on
individual capabilities considered independently.

Higher-strength combinatorial testing can expose interactions beyond
pairs, but the required test space grows rapidly as the interaction
strength and number of parameters increase [@kuhn2008beyond]. SCIF
addresses a related cost problem from a different direction. Instead of
constructing complete fixed-strength coverage for every interaction order,
it begins with lower-order stochastic screening and increases search
complexity only when unexplained residual risk remains.

## 2. Failure-Inducing Interaction Localization

Detecting a failing configuration does not by itself identify the minimal
combination responsible for the failure.

Nie and Leung formalized the Minimal Failure-Causing Schema (MFS) for
combinatorial testing, providing a framework for identifying minimal
parameter-value combinations associated with failure
[@nie2011mfs].

Several subsequent approaches improve this localization process.

Zhang and Zhang proposed Faulty Interaction Characterization (FIC) and
FIC-BS, which generate new test cases adaptively based on previous
outcomes in order to identify failure-causing parameter interactions
[@zhang2011fic].

Shakya et al. likewise augment existing combinatorial test results with
additional tests and classification in order to isolate
failure-inducing combinations [@shakya2012isolating].

Error-locating arrays and adaptive algorithms provide another
combinatorial perspective on locating interaction faults
[@martinez2009ela].

These methods establish that adaptive test generation and interaction
localization are well-developed ideas. Consequently, SCIF does not claim
novelty simply from adaptively generating additional tests or from seeking
minimal failure-causing combinations.

SCIF instead focuses on a stochastic setting in which the same
configuration is repeatedly executed to estimate failure risk and in which
the currently discovered interactions are explicitly suppressed before
the algorithm decides whether to escalate to a higher interaction order.

## 3. Masking and Multiple Faults

Interaction localization becomes more difficult when several faults can
affect the same test configuration.

Yilmaz et al. studied masking effects in combinatorial interaction testing
and introduced a feedback-driven adaptive process that detects potential
masking, characterizes likely causes, and generates additional tests
intended to exercise combinations without those likely causes
[@yilmaz2014masking].

Niu et al. subsequently showed that multiple faults can trigger masking
effects that interfere with traditional MFS identification and proposed
an MFS model and supporting approach designed for the multiple-fault
setting [@niu2020multiple].

They also proposed an interleaving framework in which combinatorial test
generation and failure-inducing interaction identification provide
feedback to each other rather than occurring as completely separate
phases [@niu2020interleaving].

The theory of pending schemas further examines unresolved interactions,
including challenges involving multiple overlapping MFSs, high-degree
interactions, and large parameter spaces [@niu2022pending].

These studies are particularly relevant to the OVERLAP and MIXED
benchmarks in BSIB. They also mean that masking and multiple-fault
localization cannot themselves be treated as new contributions of SCIF.

The distinction explored by SCIF is narrower. Once lower-order
interactions have been discovered, SCIF constructs suppression
configurations that disable those known interactions and then directly
measures whether a substantial stochastic failure signal remains. The
remaining empirical risk is used as a gate for higher-order search.

## 4. Statistical and Probabilistic Fault Localization

Most classical failure-inducing-schema formulations operate on test
outcomes associated with candidate schemas. Later work has incorporated
statistical or probabilistic reasoning into interaction localization.

The Probabilistic Failure-Causing Schema (PFS) model explicitly represents
probabilistic evidence for failure-causing schemas. Empirical comparison
between MFS and PFS has shown different precision and recall behavior
[@wang2019pfs].

BayesFLo takes a Bayesian approach and produces probabilistic rankings of
suspicious input combinations for software fault localization
[@ji2023bayesflo].

More recently, Nishiura et al. proposed FROGa and FROGb, which use
logistic-regression coefficients to estimate the suspiciousness of
failure-inducing combinations and to reduce the search space for larger
interactions [@nishiura2024frog].

Therefore, the use of probability or statistical modeling in fault
localization is also not unique to SCIF.

The stochastic role in SCIF is different from a ranking-only use of
probability. Repeated executions provide empirical failure-rate estimates
for configurations. These estimates are used both to confirm interactions
through excess risk over lower-order subsets and to determine whether
risk remains after already-discovered interactions have been suppressed.

Thus probability estimates participate directly in the control flow of
the discovery procedure.

## 5. Minimality, Delta Debugging, and Hitting Sets

Delta Debugging established a general strategy for simplifying a failing
input until a minimal failure-inducing input or difference remains
[@zeller2002delta].

SCIF's residual higher-order localizer is related to this broader family
of removal-based reasoning: capabilities are removed and the resulting
change in empirical failure probability is measured.

However, direct deletion can be confounded when several interactions are
simultaneously active. This motivates applying removal-based localization
only after already-discovered interactions have been suppressed in SCIF.

A particularly important recent comparison is NoPend by Xie et al.,
which addresses completeness, soundness, and scalability in MFS
identification and uses minimal hitting-set generation as part of its
pending-space reasoning [@xie2026nopend].

This prior work means that minimal hitting sets are not themselves a novel
algorithmic contribution of SCIF.

Their role in SCIF is specific: hitting sets are used to construct
configurations that disable all currently known pairwise interactions.
Those configurations are then executed repeatedly to estimate residual
stochastic risk. The hitting set is therefore part of the
explained-risk-suppression stage rather than the final MFS-identification
objective itself.

## 6. Reliability of Tool-Augmented AI Systems

The capability terminology used by BSIB is motivated by increasingly
tool-augmented AI systems.

FAIL-TaLMs evaluates failures caused by under-specified queries and
unavailable tools across single- and multi-tool settings
[@trevino2025failtalms].

Other work has shown that language models can also struggle to recognize
silent errors produced by faulty tools [@sun2024toolsfail].

These benchmarks demonstrate that reliability evaluation of tool-enabled
AI systems requires more than measuring ordinary text-generation
quality. However, their primary goal is to characterize or benchmark
tool-use failures rather than to identify minimal stochastic interactions
among system capabilities.

BSIB and SCIF therefore occupy a complementary experimental role: BSIB
provides controlled hidden interaction structure, while SCIF investigates
how efficiently those interaction structures can be localized from
repeated stochastic outcomes.

## 7. Positioning of SCIF

Taken together, prior work already establishes:

- t-way combinatorial interaction testing;
- minimal failure-causing schemas;
- adaptive interaction characterization;
- test augmentation for fault localization;
- masking-aware combinatorial testing;
- multiple-fault MFS reasoning;
- interleaved test generation and localization;
- probabilistic and statistical fault localization;
- removal-based failure minimization; and
- minimal-hitting-set reasoning for MFS identification.

Accordingly, the contribution of SCIF v0.0.4 should not be framed as the
first method for adaptive combinatorial testing, higher-order
localization, masking mitigation, probabilistic fault localization, or
hitting-set-based fault identification.

The specific design evaluated in this work is a
**residual-risk-guided stochastic discovery pipeline**.

Its defining sequence is:

1. repeatedly sample low-order configurations;
2. identify and statistically confirm pairwise interactions;
3. construct configurations that suppress the interactions already
   discovered;
4. repeatedly execute those residual configurations;
5. measure whether substantial unexplained failure risk remains; and
6. invoke higher-order localization only when residual evidence
   justifies escalation.

This staged use of residual stochastic risk provides the principal
positioning of SCIF relative to the prior methods reviewed above.

The present study therefore evaluates whether residual-risk-guided
escalation can preserve strong interaction recovery while avoiding the
full execution cost of exhaustive higher-order enumeration.

---

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

---

# Methodology

## 1. Problem Formulation

Let

\[
K = \{k_1, k_2, \ldots, k_n\}
\]

denote the set of capabilities available to a system.

A capability configuration is a subset

\[
C \subseteq K.
\]

Executing configuration \(C\) produces a stochastic binary outcome

\[
Y(C) \in \{0,1\},
\]

where \(Y(C)=1\) denotes a failure.

Each configuration therefore has an unknown failure probability

\[
p(C)=P(Y(C)=1).
\]

The discovery problem is to identify minimal subsets of capabilities
whose joint activation causes a substantial increase in failure risk,
while minimizing the total number of stochastic executions required.

## 2. Stochastic Capability Interactions

A capability interaction is not defined only by a high absolute
failure probability.

A candidate set must also exhibit risk beyond that observed in its
relevant lower-order subsets.

For a candidate interaction \(C\), SCIF uses a joint-risk increment
concept of the form

\[
JRI(C)
=
\hat{p}(C)
-
\max_{S \subset C}
\hat{p}(S),
\]

where \(\hat{p}\) denotes an empirical failure-rate estimate.

A candidate is therefore supported when its joint failure rate is
sufficiently large and its observed risk cannot be explained by a
lower-order subset.

## 3. BSIB Benchmark Model

The Benchmark for Stochastic Interaction Bugs (BSIB) provides
synthetic capability configurations with hidden interaction faults.

The simulator exposes only stochastic execution outcomes to the
discovery algorithm.

The underlying true failure probability is not included in the
execution result.

This prevents the discovery algorithm from directly accessing the
benchmark ground truth.

## 4. Keyed Stochastic Simulation

Experiments use deterministic keyed random streams.

For a fixed benchmark configuration and experiment seed, the random
outcome stream is stable even when configurations are evaluated in a
different order.

This design prevents algorithmic execution order from unintentionally
changing the stochastic evidence observed for the same configuration.

The keyed simulator therefore supports reproducible and fair
comparisons among discovery methods.

## 5. Pairwise Discovery

SCIF v0.0.4 begins with the SCIF v0.0.3 pairwise discovery procedure.

The frozen evaluation configuration uses:

- 100 initial screening trials;
- 300 screening-retest trials;
- 1,500 confirmation trials;
- 1,000 subset-confirmation trials;
- minimum joint failure rate of 0.15;
- minimum joint-risk increment of 0.10; and
- confidence threshold of 0.95.

Initial sampling provides a low-cost estimate of the failure signal.

Pairs with sufficiently convincing evidence proceed to confirmation.

Borderline configurations may receive additional screening trials
before a final decision is made.

This architecture concentrates stochastic executions on configurations
that show evidence of interaction risk.

## 6. Limitation of Pairwise-Only Discovery

A pure higher-order interaction can remain invisible to every
lower-order subset.

For example, consider a three-way interaction involving capabilities

\[
\{a,b,c\}.
\]

It is possible for

\[
p(\{a,b\}),
p(\{a,c\}),
p(\{b,c\})
\]

to remain near baseline while

\[
p(\{a,b,c\})
\]

is substantially elevated.

A pairwise-only algorithm therefore cannot represent or recover this
type of fault.

This limitation motivates the higher-order stages of SCIF v0.0.4.

## 7. Known-Pair Suppression

After pairwise discovery, SCIF v0.0.4 constructs probe configurations
intended to disable already-discovered pairwise interactions.

For the set of discovered pairwise interactions, the algorithm
computes minimal capability-removal sets that intersect every known
pair.

Removing such a set creates a configuration in which the discovered
pairwise interactions are suppressed.

Multiple minimal removal sets may exist.

SCIF evaluates the resulting residual configurations rather than
assuming that one particular suppression is sufficient.

## 8. Residual-Risk Detection

Let \(C_r\) denote a configuration after suppression of known pairwise
interactions.

SCIF estimates

\[
\hat{p}(C_r)
\]

and compares the remaining failure signal with the estimated baseline.

Higher-order escalation is triggered only when residual failure risk
remains sufficiently large.

The frozen parameters are:

- 1,000 residual trials;
- minimum residual failure rate of 0.15; and
- minimum residual-risk increment of 0.10.

Conceptually, the residual stage asks:

> After explaining and suppressing the interactions already found,
> does substantial unexplained risk remain?

If the answer is no, SCIF terminates without invoking higher-order
localization.

If the answer is yes, the residual configuration becomes the input to
the higher-order localizer.

## 9. Residual Higher-Order Localization

Higher-order localization is applied only after residual-risk
detection has justified escalation.

For each capability in the selected residual configuration, SCIF
measures the failure rate after removing that capability.

Let \(C_r\) be the source configuration and let \(k \in C_r\).

The empirical removal drop is

\[
D(k)
=
\hat{p}(C_r)
-
\hat{p}(C_r \setminus \{k\}).
\]

Capabilities whose removal causes a sufficiently large decrease in
failure risk are treated as candidate members of the hidden
interaction.

The frozen localization configuration uses:

- 1,000 trials per configuration;
- minimum failure rate of 0.15;
- minimum removal drop of 0.10; and
- minimum higher-order candidate size of three.

## 10. Minimality Confirmation

Removal evidence alone is not sufficient.

The resulting candidate is evaluated directly, and its immediate
subsets are also tested.

The purpose is to verify that the candidate itself retains elevated
failure risk while dropping one of its essential members removes the
interaction signal.

This step protects against reporting unnecessarily large interaction
sets.

## 11. Complete SCIF v0.0.4 Pipeline

The final procedure is:

1. perform adaptive pairwise discovery;
2. record confirmed pairwise interactions;
3. construct minimal suppression sets for the known pairs;
4. evaluate residual-risk probes;
5. stop when no substantial residual risk remains;
6. otherwise select a residual configuration;
7. apply deletion-style higher-order localization;
8. confirm candidate minimality; and
9. return pairwise and higher-order discoveries in a unified report.

The higher-order stage is therefore conditional rather than mandatory.

This design preserves the efficiency of pairwise discovery on simple
scenarios while providing an escalation path for unexplained
higher-order risk.

---

# Experimental Setup

## 1. Benchmark Scenarios

The primary evaluation uses seven BSIB scenarios.

### NULL

`BSIB-NULL-001` contains no hidden interaction.

It evaluates whether the method avoids reporting interactions when
all configurations remain near baseline stochastic risk.

### PAIR-001

`BSIB-PAIR-001` contains a strong pairwise interaction between:

- `tools`; and
- `structured_output`.

### PAIR-002

`BSIB-PAIR-002` contains a weaker pairwise interaction between:

- `tools`; and
- `streaming`.

This scenario is specifically useful for evaluating stochastic
screening robustness.

### PAIR-003

`BSIB-PAIR-003` contains an interaction between:

- `parallel_tools`; and
- `strict_schema`.

It serves as an additional unseen pairwise scenario.

### OVERLAP

`BSIB-OVERLAP-001` contains two pairwise interactions that share one
capability:

- `tools + streaming`; and
- `streaming + strict_schema`.

The scenario tests whether the discovery procedure can recover more
than one overlapping pair.

### TRIPLE

`BSIB-TRIPLE-001` contains the pure higher-order interaction:

- `tools + streaming + strict_schema`.

Its proper pairs remain near baseline.

The scenario therefore provides no pairwise interaction signal for the
hidden triple.

### MIXED

`BSIB-MIXED-001` contains both:

- pair: `tools + streaming`; and
- triple: `reasoning + strict_schema + multimodal`.

The benchmark is designed to expose masking behavior that affects
single-interaction deletion localization.

## 2. Evaluation Metrics

The principal metric is exact recovery.

A run is counted as exactly recovered only when the complete set of
reported interactions equals the benchmark ground truth.

Additional measures include:

- pairwise recovery;
- higher-order recovery;
- residual-risk classification;
- false-positive runs;
- mean simulator executions;
- median simulator executions;
- minimum and maximum executions;
- 95th-percentile execution count;
- reduction relative to exhaustive discovery; and
- wall-clock time in the scaling experiment.

## 3. Unseen Holdout Evaluation

The primary holdout evaluation uses 1,000 unseen seeds per benchmark
scenario.

The holdout seed range is:

\[
31001,\ldots,32000.
\]

Seven scenarios are evaluated, producing a total of

\[
7 \times 1000 = 7000
\]

SCIF v0.0.4 holdout runs.

Parameters were not modified after observing the holdout results.

This is important because one rare weak-pair miss was retained and
analyzed rather than being used to retune the algorithm.

## 4. Baseline Comparison

Four discovery methods are compared:

1. SCIF v0.0.3;
2. deletion-based localization;
3. exhaustive discovery; and
4. SCIF v0.0.4.

The comparison study uses 100 seeds from:

\[
41001,\ldots,41100.
\]

The selected scenarios are:

- PAIR-002;
- OVERLAP;
- TRIPLE; and
- MIXED.

For pairwise scenarios, exhaustive discovery evaluates configurations
through order two.

For scenarios containing a triple, exhaustive discovery evaluates
configurations through order three.

With eight capabilities this corresponds to:

\[
1 + 8 + {8 \choose 2}
=
37
\]

configurations for exhaustive order-two discovery, or 37,000
simulator executions at 1,000 trials per configuration.

For exhaustive order-three discovery:

\[
1 + 8 + {8 \choose 2} + {8 \choose 3}
=
93
\]

configurations are evaluated, corresponding to 93,000 simulator
executions.

## 5. Ablation Study

The ablation study uses 100 seeds:

\[
51001,\ldots,51100.
\]

Five representative scenarios are evaluated:

- NULL;
- PAIR-002;
- OVERLAP;
- TRIPLE; and
- MIXED.

Three algorithmic stages are compared:

### Stage A — V3 Pairwise Only

Only confirmed pairwise discoveries are considered.

### Stage B — V3 + Residual Detection

Pairwise discovery is followed by residual-risk classification.

This stage determines whether higher-order escalation is needed but
does not yet localize a higher-order interaction.

### Stage C — Full V4

The complete pipeline includes residual higher-order localization.

The ablation records:

- stage success;
- false residual escalations;
- missed escalations;
- false higher-order candidates; and
- mean execution cost.

## 6. Sensitivity Study

The sensitivity study uses 100 seeds:

\[
61001,\ldots,61100.
\]

Four scenarios are tested:

- NULL;
- PAIR-002;
- TRIPLE; and
- MIXED.

The frozen baseline configuration is:

- `initial_trials = 100`;
- `min_residual_increment = 0.10`; and
- `higher_order_min_removal_drop = 0.10`.

The evaluated alternatives are:

- initial trials = 50;
- initial trials = 200;
- residual increment = 0.05;
- residual increment = 0.15;
- removal drop = 0.05; and
- removal drop = 0.15.

The purpose is robustness characterization rather than post-holdout
parameter optimization.

## 7. Scaling Study

Scaling is evaluated using benchmark variants with:

- 8 capabilities;
- 12 capabilities;
- 16 capabilities; and
- 20 capabilities.

Each benchmark retains:

- one pairwise interaction; and
- one three-way interaction.

Additional capabilities are non-interacting noise capabilities.

Twenty seeds are evaluated for each size:

\[
71001,\ldots,71020.
\]

For \(n\) capabilities, exhaustive order-three discovery evaluates

\[
1+n+{n \choose 2}+{n \choose 3}
\]

configurations.

At 1,000 trials per configuration, exhaustive execution counts are:

- 93,000 for 8 capabilities;
- 299,000 for 12 capabilities;
- 697,000 for 16 capabilities; and
- 1,351,000 for 20 capabilities.

## 8. Reproducibility

The implementation is maintained in the Berliant repository.

The frozen research milestone is identified by the Git tag:

`scif-v0.0.4`

The repository includes:

- benchmark definitions;
- simulator implementation;
- discovery algorithms;
- automated tests;
- experiment scripts;
- aggregated result files; and
- publication figure-generation scripts.

All Python development commands are executed through the project's
`uv` environment.

---

# Results

## 1. RQ1 — Holdout Discovery Accuracy

![SCIF V4 exact recovery on the 1,000-seed unseen holdout.](../results/paper/figures/figure_5_holdout_recovery.png)

*Figure 1. SCIF v0.0.4 exact recovery across the seven 1,000-seed unseen holdout scenarios.*


SCIF v0.0.4 achieved near-perfect exact recovery across the unseen
1,000-seed holdout evaluation.

**Table 1. Holdout exact recovery and execution cost.**

| Scenario | Exact Recovery | False-Positive Runs | Mean Executions |
|---|---:|---:|---:|
| NULL | 1000/1000 (100.0%) | 0/1000 | 4,907.6 |
| PAIR-001 | 1000/1000 (100.0%) | 0/1000 | 10,800.0 |
| PAIR-002 | 999/1000 (99.9%) | 0/1000 | 10,946.2 |
| PAIR-003 | 1000/1000 (100.0%) | 0/1000 | 10,846.2 |
| OVERLAP | 1000/1000 (100.0%) | 0/1000 | 13,100.0 |
| TRIPLE | 1000/1000 (100.0%) | 0/1000 | 17,712.3 |
| MIXED | 1000/1000 (100.0%) | 0/1000 | 22,803.2 |

Across all seven scenarios, SCIF v0.0.4 obtained

\[
6999 / 7000
=
99.9857\%
\]

exact recovery.

The corresponding 95% Wilson score interval was approximately

\[
99.9191\%
\text{ to }
99.9975\%.
\]

For scenarios with 1000/1000 observed exact recovery, the corresponding
95% Wilson interval was approximately 99.6173% to 100%. Thus, observed
100% recovery is not interpreted as evidence that the underlying error
probability is exactly zero.

No false interaction candidate was observed in the 7,000 holdout runs.

The result indicates that the method preserved strong recovery across
null, pairwise, overlapping-pair, pure-triple, and mixed-order
settings.

## 2. Rare PAIR-002 Holdout Miss

The only exact-recovery miss occurred in `PAIR-002` at seed 31269.

During the initial 100-trial screening stage, the observations were:

- target-pair failures: 10/100;
- target-pair failure rate: 0.100;
- baseline failure rate: 0.100; and
- observed joint-risk increment: 0.000.

The true weak pair therefore appeared indistinguishable from baseline
in this particular initial stochastic sample and was not promoted for
additional pairwise evaluation.

The residual stage subsequently observed a residual failure rate of
0.242 and correctly recognized unexplained risk.

However, higher-order localization did not report a false interaction.

The final run therefore represented a false negative for the weak
pair, not a false interaction discovery.

The parameters were deliberately left unchanged after observing this
holdout failure.

## 3. RQ2 — Comparison with Discovery Baselines

![Exact interaction recovery by discovery method.](../results/paper/figures/figure_1_recovery_comparison.png)

*Figure 2. Exact recovery of SCIF V3, deletion localization, exhaustive discovery, and SCIF V4.*

![Simulator execution cost by discovery method.](../results/paper/figures/figure_2_execution_comparison.png)

*Figure 3. Mean simulator executions required by each discovery method.*


The method-comparison experiment shows that no evaluated baseline
provided the same behavior across all four representative interaction
structures.

**Table 2. Method comparison over 100 seeds per scenario.**

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

### Pairwise scenario

On PAIR-002, both SCIF V3 and V4 reached 100% recovery.

V3 required fewer executions because it terminates after pairwise
discovery, whereas V4 additionally performs residual-risk verification.

### Overlapping pairwise interactions

SCIF V3 and V4 both recovered the two overlapping pairs in every run.

Deletion localization failed because the benchmark does not contain a
single dominant interaction that can be isolated through the removal
criterion used by that baseline.

### Pure triple

Pairwise SCIF recovered none of the pure triple interactions because
the proper pairwise subsets remained near baseline.

Deletion recovered the isolated triple in all 100 runs.

SCIF V4 also achieved 100% exact recovery while requiring a mean of
17,700 executions compared with 93,000 for exhaustive order-three
discovery.

This corresponds to an execution reduction of approximately 80.97%.

### Mixed-order interaction

The MIXED benchmark produced the clearest architectural distinction.

SCIF V3 recovered the pairwise interaction but could not represent the
hidden triple, resulting in 0% exact recovery.

Deletion localization also produced 0% exact recovery because the
pairwise interaction masked removal evidence from the higher-order
fault.

Exhaustive discovery obtained 100% recovery at 93,000 executions.

SCIF V4 obtained the same exact recovery with 22,800 mean executions,
representing a reduction of approximately 75.48%.

## 4. RQ3 — Ablation of Residual-Risk Reasoning

The ablation experiment isolates the contribution of the two new
higher-order stages.

**Table 3. Ablation of residual-risk detection and localization.**

| Scenario | V3 Pairwise Only | V3 + Residual | Full V4 |
|---|---:|---:|---:|
| NULL | 100% | 100% | 100% |
| PAIR-002 | 100% | 100% | 100% |
| OVERLAP | 100% | 100% | 100% |
| TRIPLE | 0% | 100% correct escalation | 100% exact recovery |
| MIXED | 0% | 100% correct escalation | 100% exact recovery |

Across all 500 ablation runs:

- false residual escalations: 0;
- missed residual escalations: 0; and
- false higher-order candidates: 0.

The results separate two functions of the V4 extension.

First, residual-risk detection determines whether the currently
discovered interactions fully explain the observed risk.

Second, higher-order localization identifies the exact interaction
responsible for unexplained residual risk.

For TRIPLE, mean execution counts were:

- V3 only: 3,700;
- V3 + residual: 4,700; and
- full V4: 17,700.

For MIXED they were:

- V3 only: 7,800;
- V3 + residual: 10,800; and
- full V4: 22,800.

Higher-order localization therefore adds cost only when escalation is
required.

## 5. RQ4 — Parameter Sensitivity

The default configuration achieved 100% exact recovery on all four
sensitivity scenarios.

Changing the residual-risk increment from 0.10 to either 0.05 or 0.15
did not reduce exact recovery in this experiment.

Similarly, increasing the higher-order minimum removal drop from 0.10
to 0.15 retained 100% exact recovery.

The principal sensitivity appeared when the removal threshold was
reduced to 0.05.

Under this setting:

- TRIPLE exact recovery decreased to 95/100; and
- MIXED exact recovery decreased to 96/100.

Diagnostic analysis showed that non-essential capabilities sometimes
exhibited stochastic removal drops slightly above the permissive 0.05
threshold.

Observed examples included spurious drops in approximately the
0.05-0.075 range.

These capabilities entered oversized candidate sets.

The subsequent minimality checks rejected those candidates, producing
`None` rather than a false higher-order interaction.

Thus, the permissive threshold primarily increased false-negative
localization rather than false-positive reporting.

The frozen value of 0.10 was retained.

## 6. RQ5 — Scaling Behavior

![SCIF V4 execution scaling compared with exhaustive order-three search.](../results/paper/figures/figure_3_scaling.png)

*Figure 4. Simulator execution scaling from 8 to 20 capabilities.*

![Execution reduction relative to exhaustive discovery.](../results/paper/figures/figure_4_scaling_reduction.png)

*Figure 5. Relative execution reduction of SCIF V4 compared with exhaustive order-three discovery.*


SCIF v0.0.4 obtained 20/20 exact recoveries for every tested
capability count in the scaling experiment. Because each capability
count used only twenty seeds, the 95% Wilson interval associated with
20/20 recovery is approximately 83.89% to 100%. The scaling recovery
results should therefore be interpreted as initial robustness evidence
rather than as precise estimates of the underlying recovery probability.

**Table 4. Scaling of recovery and simulator execution cost.**

| Capabilities | Exact Recovery | Mean SCIF V4 Executions | Exhaustive Executions | Reduction |
|---:|---:|---:|---:|---:|
| 8 | 20/20 (100%) | 22,800 | 93,000 | 75.48% |
| 12 | 20/20 (100%) | 31,000 | 299,000 | 89.63% |
| 16 | 20/20 (100%) | 40,800 | 697,000 | 94.15% |
| 20 | 20/20 (100%) | 52,200 | 1,351,000 | 96.14% |

The execution advantage increased with the size of the capability
space.

From 8 to 20 capabilities, exhaustive order-three execution cost grew
from 93,000 to 1,351,000 executions.

Over the same range, SCIF v0.0.4 increased from 22,800 to 52,200 mean
executions.

The relative execution reduction consequently increased from 75.48%
at eight capabilities to 96.14% at twenty capabilities.

## 7. Wall-Clock Scaling

Mean runtime in the synthetic scaling experiment was:

- 0.2282 seconds at 8 capabilities;
- 0.3179 seconds at 12 capabilities;
- 0.5400 seconds at 16 capabilities; and
- 2.6731 seconds at 20 capabilities.

The increase between 16 and 20 capabilities is substantially larger
than the increase in simulator execution count alone.

This behavior is consistent with the current implementation's
enumeration of minimal hitting sets during pair suppression.

The result therefore identifies a computational optimization target
for larger capability spaces even though SCIF remains substantially
more execution-efficient than exhaustive discovery.

## 8. Summary of Findings

The experiments provide the following answers to the research
questions.

**RQ1:** SCIF v0.0.4 achieved 99.9857% exact recovery across 7,000
unseen holdout runs with no observed false interaction candidates.

**RQ2:** SCIF v0.0.4 matched exhaustive recovery in the representative
100-seed comparison while substantially reducing simulator executions.
Unlike V3 and deletion localization, it recovered the tested mixed
pairwise-plus-triple scenario.

**RQ3:** Residual-risk detection correctly identified when
higher-order escalation was necessary, while residual localization
converted that evidence into exact higher-order recovery.

**RQ4:** The frozen parameters were stable across the tested
sensitivity range. A removal threshold of 0.05 was shown to be too
permissive to stochastic removal noise.

**RQ5:** SCIF obtained 20/20 exact recoveries at each tested
capability count from 8 through 20 capabilities, while execution
reduction relative to exhaustive order-three search increased from
75.48% to 96.14%. Because the scaling study uses only twenty seeds per
size, these recovery results have wider statistical uncertainty than
the main holdout evaluation.

---

# Discussion

## 1. Main Interpretation

The experimental results suggest that the central advantage of SCIF
v0.0.4 is not simply a stronger higher-order search procedure.

Its primary contribution is the separation of already-explained risk
from unexplained residual risk.

Pairwise discovery remains the first stage because many interaction
faults can be identified efficiently at order two.

Higher-order localization is invoked only when evidence remains after
known pairwise interactions have been suppressed.

This conditional escalation allows the method to retain relatively
low execution cost on simple scenarios while still representing
higher-order interactions when required.

## 2. Pairwise Discovery Remains Valuable

The comparison results show that SCIF v0.0.3 is highly effective when
the underlying interaction structure is pairwise.

For PAIR-002, V3 achieved 100% recovery in the 100-seed method
comparison using approximately 7,900 mean executions.

SCIF v0.0.4 required approximately 10,900 executions because it also
performed residual-risk verification.

This overhead is intentional.

V4 pays additional cost to determine whether the pairwise discoveries
fully explain the risk landscape.

Consequently, V4 should not be interpreted as uniformly cheaper than
its pairwise predecessor.

Instead, it trades a modest verification cost for the ability to
detect when pairwise reasoning is insufficient.

## 3. Why Pure Higher-Order Interactions Require Escalation

The TRIPLE benchmark demonstrates an architectural limitation of
pairwise-only discovery.

The three-way interaction is constructed so that its pairwise subsets
remain near baseline.

No amount of improved pairwise ranking can recover an interaction that
does not produce pairwise evidence.

The 0% exact recovery of V3 on this scenario is therefore not merely a
parameter failure.

It reflects a representational limitation.

SCIF v0.0.4 addresses this by evaluating the residual configuration
after pairwise discovery has failed to explain the observed risk.

Once substantial residual risk is detected, the higher-order
localizer identifies capabilities whose removal collapses the risk.

This enables exact recovery of the hidden triple.

## 4. Why Mixed-Order Interactions Are More Difficult

The MIXED scenario is particularly important because it contains both
a pairwise and a three-way interaction.

The pairwise fault is readily discovered by V3.

However, discovering the pair does not imply that all observed risk is
now explained.

A full configuration may still contain the independent three-way
fault.

Deletion localization also struggles in this setting.

When deletion is applied directly to a configuration containing
multiple active interactions, removing a member of one interaction
may leave another interaction active.

The remaining failure probability can therefore stay high enough to
hide the importance of the removed capability.

SCIF v0.0.4 reduces this masking problem by first suppressing the
known pair.

Localization then operates inside a residual configuration in which
the already-explained pairwise interaction has been disabled.

In the tested mixed benchmark, this separation is sufficient to expose
the hidden triple.

## 5. Interpretation of the Ablation Study

The ablation study provides evidence that the two new stages perform
distinct roles.

Pairwise discovery alone was sufficient for NULL, PAIR-002, and
OVERLAP, but it could not produce exact recovery for TRIPLE or MIXED.

Adding residual-risk detection did not yet localize the triple.

Instead, it correctly answered a different question:

> Is there important risk that the current discoveries do not explain?

For both TRIPLE and MIXED, this decision was correct in all 100
ablation seeds.

The localization stage then converted that residual evidence into an
exact higher-order candidate.

This separation is useful because it prevents expensive higher-order
localization from being executed indiscriminately.

## 6. Interpretation of the Weak-Pair Holdout Miss

The only exact-recovery failure across the 7,000 unseen holdout runs
occurred on PAIR-002 at seed 31269.

The target pair produced only 10 failures in its first 100 trials,
while the baseline configuration also produced 10 failures.

The resulting empirical joint-risk increment was therefore zero.

The pair was not promoted beyond initial screening.

This case illustrates an unavoidable property of stochastic
screening: a finite initial sample can occasionally obscure a real
effect.

Importantly, residual-risk detection subsequently recognized that
substantial unexplained risk remained.

The higher-order localizer then declined to report an unsupported
higher-order candidate.

Thus, the error remained a false negative rather than becoming a false
positive.

Retaining this failure without modifying the parameters after holdout
inspection provides a more realistic estimate of the frozen method's
performance.

## 7. Sensitivity and Conservative Localization

The sensitivity experiment shows that the higher-order removal
threshold has a meaningful role.

At the default value of 0.10, exact recovery remained 100% across the
tested sensitivity scenarios.

Increasing the threshold to 0.15 also preserved exact recovery.

Reducing it to 0.05 caused recovery to fall to 95% on TRIPLE and 96%
on MIXED.

Diagnostic runs showed that irrelevant capabilities sometimes
exhibited stochastic removal drops between approximately 0.05 and
0.075.

At the permissive threshold, these capabilities entered the candidate
set.

The minimality check subsequently rejected the oversized candidate.

This behavior suggests that conservative removal filtering is
important because the localization stage operates on empirical
probabilities rather than deterministic effects.

## 8. Efficiency Relative to Exhaustive Search

Exhaustive discovery is valuable as an oracle-style baseline because
it systematically evaluates every configuration up to the selected
interaction order.

Its primary disadvantage is combinatorial growth.

For eight capabilities, exhaustive order-three discovery requires
93,000 executions under the experimental protocol.

For twenty capabilities, the requirement becomes 1,351,000.

SCIF v0.0.4 required a mean of only 52,200 executions at twenty
capabilities in the scaling benchmark.

The relative reduction increased from 75.48% at eight capabilities to
96.14% at twenty capabilities.

The increasing percentage reduction is expected because exhaustive
order-three configuration count grows combinatorially, whereas much
of the SCIF pipeline performs targeted pairwise screening and
conditional residual evaluation.

## 9. Execution Efficiency Is Not the Same as Computational Complexity

The scaling experiment also reveals an important distinction between
simulator execution efficiency and algorithmic overhead.

Mean wall-clock time increased from approximately 0.23 seconds at
eight capabilities to 2.67 seconds at twenty capabilities.

The increase is larger than would be expected from simulator
executions alone.

One likely contributor is the current enumeration of minimal hitting
sets used for pair suppression.

Therefore, the current results should not be interpreted as evidence
that every internal operation scales linearly.

Rather, the experiments show that the number of expensive stochastic
simulator executions remains substantially below exhaustive
order-three enumeration over the tested range.

Improving the hitting-set implementation is an important direction for
future optimization.

## 10. Implications

The results support a broader design principle for stochastic system
debugging.

When multiple interaction orders may coexist, discovery need not begin
with unrestricted high-order enumeration.

A potentially more efficient strategy is:

1. discover simple interactions first;
2. explicitly suppress or condition on what has already been
   explained;
3. measure whether meaningful residual risk remains; and
4. escalate search complexity only when the residual evidence
   requires it.

The current SCIF implementation demonstrates this principle for
pairwise and selected three-way interaction structures.

Whether the same idea generalizes to larger and more complex
production systems remains an empirical question.

---

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

---

# Conclusion

This work investigated the discovery of stochastic capability
interactions without relying on exhaustive low-order enumeration.

The proposed SCIF v0.0.4 pipeline combines adaptive pairwise discovery
with known-pair suppression, residual-risk detection, and conditional
higher-order localization.

The central design principle is that search complexity should increase
only when the currently discovered interactions fail to explain the
remaining stochastic risk.

Evaluation on the BSIB benchmark family showed that SCIF v0.0.4 can
represent interaction structures that are inaccessible to pairwise-only
discovery and difficult for direct deletion localization.

Across 7,000 unseen holdout runs, the method achieved 6,999 exact
recoveries, corresponding to 99.9857%, with no observed false
interaction candidates.

The only holdout miss occurred on a deliberately weaker pairwise
interaction whose first 100 stochastic trials happened to produce the
same empirical failure rate as baseline.

In the representative method comparison, SCIF v0.0.4 achieved 100%
exact recovery on pairwise, overlapping, pure-triple, and mixed-order
scenarios.

Pairwise SCIF failed on the pure-triple and mixed scenarios, while
deletion localization failed on the overlapping and mixed settings.

Exhaustive discovery recovered all evaluated structures but required
substantially more simulator executions.

The ablation study showed that residual-risk detection and
higher-order localization contribute distinct functionality.

Residual-risk detection correctly determined when pairwise discoveries
left important risk unexplained, while localization converted that
residual signal into an exact higher-order candidate.

The scaling experiment further showed that execution savings relative
to exhaustive order-three discovery increased as the capability space
grew, reaching 96.14% at twenty capabilities in the evaluated
benchmark.

These results support residual-risk-guided escalation as a promising
strategy for stochastic interaction discovery.

At the same time, the current work remains an early research
prototype.

Future work should evaluate multiple overlapping higher-order
interactions, alternative fault-composition models, larger capability
spaces, more efficient hitting-set computation, broader algorithmic
baselines, and real-world AI-system failures.

Within the evaluated synthetic setting, SCIF v0.0.4 demonstrates that
strong mixed-order interaction recovery can be achieved without
paying the full execution cost of exhaustive combinatorial search.
