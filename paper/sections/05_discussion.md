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
