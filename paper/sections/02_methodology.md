# Methodology

## Problem Formulation

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

## Stochastic Capability Interactions

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
\max_{S \subsetneq C}
\hat{p}(S),
\]

where \(\hat{p}\) denotes an empirical failure-rate estimate and
the maximum is taken over proper lower-order subsets of \(C\). For a
pair, these comparison configurations are the baseline and the two
singleton capabilities.

A candidate is therefore supported when its joint failure rate is
sufficiently large and its observed risk cannot be explained by a
lower-order subset.

## BSIB Benchmark Model

The Benchmark for Stochastic Interaction Bugs (BSIB) provides
synthetic capability configurations with hidden interaction faults.

The simulator exposes only stochastic execution outcomes to the
discovery algorithm.

The underlying true failure probability is not included in the
execution result.

This prevents the discovery algorithm from directly accessing the
benchmark ground truth.

## Keyed Stochastic Simulation

Experiments use deterministic keyed random streams.

For a fixed benchmark configuration and experiment seed, the random
outcome stream is stable even when configurations are evaluated in a
different order.

This design prevents algorithmic execution order from unintentionally
changing the stochastic evidence observed for the same configuration.

The keyed simulator therefore supports reproducible and fair
comparisons among discovery methods.

## Pairwise Discovery

SCIF v0.0.4 begins with the SCIF v0.0.3 pairwise discovery procedure.

The frozen evaluation configuration uses:

- 100 initial screening trials;
- 300 screening-retest trials;
- 1,500 confirmation trials;
- 1,000 subset-confirmation trials;
- minimum joint failure rate of 0.15;
- minimum joint-risk increment of 0.10;
- screening posterior-probability threshold of 0.20; and
- confirmation posterior-support threshold of 0.95.

Initial screening uses relaxed empirical thresholds equal to 75% of
the minimum joint-failure threshold and 67% of the minimum
joint-risk-increment threshold. With the frozen parameters, these are
0.1125 and 0.067, respectively.

A pair that immediately satisfies both screening thresholds proceeds
to confirmation. If its joint rate reaches the screening threshold
but its empirical JRI does not, SCIF estimates the posterior
probability that both screening conditions hold. A probability of at
least 0.20 triggers extension of the baseline, both singleton
configurations, and the pair to 300 trials before screening is
re-evaluated.

During confirmation, the baseline and singleton subsets are extended
to 1,000 trials and the candidate pair to 1,500 trials. Posterior
support is estimated from 10,000 Beta posterior samples using
Beta(f+0.5, n-f+0.5) for a configuration with f failures in n trials.
The reported confidence is the fraction of posterior samples for which
both the joint failure rate is at least 0.15 and the JRI is at least
0.10. A pair is confirmed only when its empirical thresholds are also
satisfied and this posterior support is at least 0.95.

## Limitation of Pairwise-Only Discovery

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

## Known-Pair Suppression

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

## Residual-Risk Detection

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

## Residual Higher-Order Localization

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

## Minimality Confirmation

Removal evidence alone is not sufficient.

The resulting candidate is evaluated directly, and its immediate
subsets are also tested.

The purpose is to verify that the candidate itself retains elevated
failure risk while dropping one of its essential members removes the
interaction signal.

This step protects against reporting unnecessarily large interaction
sets.

## Complete SCIF v0.0.4 Pipeline

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
