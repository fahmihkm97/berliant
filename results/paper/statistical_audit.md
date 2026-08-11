# Statistical Audit

## Confidence Interval Method

Recovery proportions are reported with 95% Wilson score intervals.

Wilson intervals are preferred here over the simple normal
approximation because several experiments contain proportions at or
near the boundary, including:

- 1000/1000;
- 100/100; and
- 20/20.

A reported empirical recovery rate of 100% should therefore not be
interpreted as proof that the underlying failure probability is zero.

## Main Holdout

Overall SCIF v0.0.4 holdout performance:

- exact recoveries: 6999/7000;
- empirical exact recovery: 99.9857%;
- 95% Wilson interval: approximately 99.9191% to 99.9975%.

For scenarios with 1000/1000 exact recovery:

- empirical recovery: 100%;
- 95% Wilson interval: approximately 99.6173% to 100%.

For PAIR-002:

- exact recovery: 999/1000;
- empirical recovery: 99.9%;
- 95% Wilson interval: approximately 99.4357% to 99.9823%.

## 100-Seed Experiments

For 100/100 recovery:

- empirical recovery: 100%;
- 95% Wilson interval: approximately 96.3007% to 100%.

For 0/100 recovery:

- empirical recovery: 0%;
- 95% Wilson interval: approximately 0% to 3.6993%.

For 2/100 recovery:

- empirical recovery: 2%;
- 95% Wilson interval: approximately 0.5502% to 7.0012%.

## Scaling Experiment

Each capability count was evaluated with 20 seeds.

For 20/20 recovery:

- empirical recovery: 100%;
- 95% Wilson interval: approximately 83.8875% to 100%.

The scaling experiment should therefore be interpreted primarily as
evidence about execution-cost trends and initial recovery robustness,
not as precise estimation of the underlying recovery probability.
