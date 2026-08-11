# SCIF v0.0.4 Claim Audit

## Claims supported by the current experiments

### Holdout accuracy

Supported:

> SCIF v0.0.4 achieved 6,999 exact recoveries in 7,000 unseen
> BSIB holdout runs.

Supported:

> The empirical exact-recovery rate was 99.9857%.

Supported:

> No false interaction candidates were observed in the 7,000
> holdout runs.

Do not rewrite this as:

> SCIF has no false positives.

The experiment only supports an observed count of zero.

## Weak-pair result

Supported:

> PAIR-002 achieved 999/1000 exact recovery.

Supported:

> The single observed miss occurred when the target pair and
> baseline both produced a 0.10 initial empirical failure rate.

Do not claim guaranteed weak-interaction recovery.

## Method comparison

Supported for the evaluated 100-seed experiment:

> SCIF V4 achieved 100/100 exact recovery on PAIR-002,
> OVERLAP, TRIPLE, and MIXED.

Supported:

> V3 failed to exactly recover TRIPLE and MIXED.

Supported:

> The deletion baseline failed to exactly recover OVERLAP
> and MIXED.

These claims must remain scoped to the evaluated BSIB scenarios.

## Efficiency

Supported:

> SCIF V4 used 22,800 mean executions on the eight-capability
> MIXED comparison versus 93,000 for exhaustive order-three
> discovery.

Supported:

> This represents a 75.48% reduction.

Do not claim general asymptotic superiority from this experiment.

## Scaling

Supported:

> SCIF achieved 20/20 exact recoveries for every tested
> capability count from 8 through 20.

Supported:

> Execution reduction increased from 75.48% at 8 capabilities
> to 96.14% at 20 capabilities.

Do not write:

> SCIF has 100% true recovery up to 20 capabilities.

Each scaling condition contains only twenty runs.

## Novelty

Do not claim:

- first adaptive combinatorial testing method;
- first failure-inducing interaction localizer;
- first masking-aware method;
- first multiple-fault interaction method;
- first probabilistic fault-localization approach;
- first higher-order interaction method;
- first use of minimal hitting sets.

Preferred positioning:

> SCIF v0.0.4 evaluates a residual-risk-guided stochastic
> discovery pipeline that suppresses already-supported
> interactions, measures unexplained empirical failure risk,
> and conditionally escalates to higher-order localization.

Until a broader systematic literature review is complete,
use language such as:

> We investigate...

> We propose...

> In the evaluated setting...

Avoid absolute priority claims.

## External validity

Current evidence is synthetic.

Do not claim that the current results establish equivalent
performance for production AI systems.

Preferred wording:

> The results establish behavior within the evaluated BSIB
> synthetic benchmark family and motivate future external
> validation on production AI systems.
