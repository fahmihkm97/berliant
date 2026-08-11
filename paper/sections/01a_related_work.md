# Related Work

## Combinatorial Testing and Interaction Localization

Combinatorial testing (CT) targets faults caused by interactions among input parameters or configuration options. Rather than enumerating every system configuration, t-way testing covers combinations up to a selected interaction strength [@kuhn2008beyond; @nie2011survey]. Higher-strength testing can expose interactions beyond pairs, but its cost increases rapidly with both interaction strength and the number of parameters.

Beyond detecting failing configurations, prior work has addressed localization of the combinations responsible for failure. Nie and Leung formalized the Minimal Failure-Causing Schema (MFS) for identifying minimal parameter-value combinations associated with failures [@nie2011mfs]. Zhang and Zhang proposed Faulty Interaction Characterization (FIC), which adaptively generates additional tests from previous outcomes [@zhang2011fic]. Shakya et al. similarly combined test augmentation and classification to isolate failure-inducing combinations [@shakya2012isolating], while error-locating arrays provide another adaptive combinatorial perspective [@martinez2009ela].

These studies establish adaptive interaction localization as prior art. SCIF addresses a narrower setting in which repeated executions estimate stochastic failure risk and search order is increased only when lower-order discoveries leave substantial unexplained risk.

## Masking and Multiple Faults

Localization becomes harder when multiple interactions can affect the same configuration. Yilmaz et al. introduced a feedback-driven adaptive approach for reducing masking effects by identifying likely causes and generating tests intended to exercise combinations without them [@yilmaz2014masking].

Niu et al. showed that multiple faults can interfere with traditional MFS identification and developed an approach specifically for multiple-fault settings [@niu2020multiple]. They later proposed an interleaving framework in which test generation and failure-inducing interaction identification exchange feedback during testing [@niu2020interleaving]. Pending-schema theory further examines unresolved, overlapping, and high-degree interactions in large configuration spaces [@niu2022pending].

These works are particularly relevant to the OVERLAP and MIXED benchmarks used in this study. SCIF differs in how already-supported interactions are used: it constructs configurations that suppress those interactions, repeatedly measures the remaining empirical failure risk, and uses that residual signal as a gate for higher-order localization.

## Statistical and Probabilistic Localization

Probabilistic reasoning has also been applied to fault localization. The Probabilistic Failure-Causing Schema model represents probabilistic evidence for candidate schemas [@wang2019pfs]. BayesFLo uses Bayesian reasoning to rank suspicious input combinations [@ji2023bayesflo], while FROG uses logistic-regression coefficients to estimate suspiciousness and reduce the search space for larger failure-inducing combinations [@nishiura2024frog].

SCIF therefore does not claim novelty from using probability alone. Its use of stochastic evidence is procedural: repeated executions estimate configuration-specific failure rates, these estimates support interaction confirmation through excess risk over lower-order subsets, and residual failure probability determines whether higher-order search is invoked.

## Minimality, Deletion, and Hitting Sets

SCIF is also related to failure-minimization techniques. Delta Debugging iteratively simplifies failing inputs to isolate minimal failure-inducing conditions [@zeller2002delta]. SCIF's higher-order localization similarly evaluates removals, but direct deletion can be misleading when several interactions are simultaneously active. SCIF therefore applies removal-based localization after suppressing interactions already supported by the data.

Recent work is especially relevant here. NoPend addresses complete, sound, and scalable MFS identification and uses minimal hitting-set generation in its pending-space reasoning [@xie2026nopend]. Minimal hitting sets are thus not themselves a contribution of SCIF. In SCIF, their role is specifically to construct configurations that disable all currently known pairwise interactions so that repeated executions can estimate how much stochastic risk remains unexplained.

## Reliability of Tool-Augmented AI Systems

BSIB's capability-oriented formulation is motivated by increasingly tool-enabled AI systems. FAIL-TaLMs evaluates failures involving under-specified queries and unavailable tools in single- and multi-tool settings [@trevino2025failtalms]. Other work shows that language models may also fail to recognize silent errors produced by faulty tools [@sun2024toolsfail].

Such benchmarks establish the importance of reliability evaluation for capability-rich AI systems, but their primary objective is to characterize tool-use failures rather than localize minimal stochastic interactions among system capabilities. BSIB instead provides controlled hidden interaction structures, enabling SCIF to be evaluated against known ground truth.

## Positioning of SCIF

Prior research therefore already establishes t-way combinatorial testing, MFS localization, adaptive test generation, masking-aware and multiple-fault methods, probabilistic fault localization, failure minimization, and hitting-set-based reasoning.

Accordingly, SCIF v0.0.4 is not positioned as the first adaptive, probabilistic, higher-order, masking-aware, or hitting-set-based interaction-localization method.

The design evaluated here is a **residual-risk-guided stochastic discovery pipeline**. It first screens and confirms lower-order interactions, constructs configurations that suppress interactions already supported by the data, repeatedly estimates the remaining failure risk, and invokes higher-order localization only when that residual evidence justifies escalation.

The experimental question is therefore whether this residual-risk-guided escalation can maintain accurate mixed-order interaction discovery while reducing simulator executions relative to exhaustive higher-order enumeration.
