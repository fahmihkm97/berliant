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
