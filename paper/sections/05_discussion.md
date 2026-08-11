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

Importantly, residual-risk detection still identified unexplained
risk, while the higher-order localizer declined to report an
unsupported candidate. The miss therefore remained a false negative
rather than becoming a false positive. We retained this outcome
without post-holdout parameter tuning.

## 7. Sensitivity and Conservative Localization

Sensitivity analysis indicates that the higher-order removal threshold
controls a meaningful noise-versus-recall trade-off. The default value
of 0.10 and the stricter value of 0.15 preserved exact recovery across
the tested scenarios, whereas reducing the threshold to 0.05 lowered
recovery on TRIPLE and MIXED.

Diagnostics showed that stochastic removal effects from irrelevant
capabilities occasionally exceeded the permissive threshold, producing
oversized candidates that were subsequently rejected by the minimality
check. This supports conservative filtering when localization relies on
empirical rather than deterministic effects.

## 8. Efficiency and Computational Cost

Exhaustive discovery remains useful as an oracle-style baseline, but
its configuration count grows combinatorially with capability count
and interaction order. SCIF instead concentrates simulator executions
on pairwise screening and conditionally invokes higher-order search
only when residual evidence requires it. The scaling experiment shows
that this strategy increasingly reduces simulator executions relative
to exhaustive order-three enumeration as capability count grows.

Execution savings should not be confused with uniformly low internal
computational complexity. Wall-clock growth was steeper than simulator
execution growth at larger capability counts, with minimal hitting-set
enumeration a likely contributor. This identifies an implementation
optimization target rather than a failure of interaction recovery.

## 9. Implications

The experiments support a residual-risk-guided strategy for stochastic
interaction discovery: identify simpler interactions first, suppress
what is already explained, measure the remaining risk, and escalate
search order only when substantial unexplained evidence remains.

SCIF v0.0.4 demonstrates this principle for the evaluated pairwise and
three-way interaction structures. Generalization to larger
interaction orders and production systems remains an open empirical
question.
