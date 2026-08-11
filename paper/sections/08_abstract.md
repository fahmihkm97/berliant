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
