from collections.abc import Callable, Sequence
from dataclasses import dataclass
from itertools import combinations

import numpy as np

from berliant.bsib import ExecutionResult

InvokeFunction = Callable[[set[str]], ExecutionResult]


@dataclass(frozen=True)
class TrialStats:
    trials: int
    failures: int

    @property
    def failure_rate(self) -> float:
        return self.failures / self.trials


@dataclass(frozen=True)
class SCIFCandidate:
    capabilities: tuple[str, str]
    joint_failure_rate: float
    max_subset_failure_rate: float
    joint_risk_increment: float
    confidence: float


@dataclass(frozen=True)
class SCIFReport:
    stats: dict[tuple[str, ...], TrialStats]
    candidates: tuple[SCIFCandidate, ...]
    executions: int


class SCIFDiscovery:
    """
    Adaptive stochastic capability-interaction discovery.

    Version 0.0.1 focuses on pairwise interactions.
    """

    def __init__(
        self,
        invoke: InvokeFunction,
        capabilities: Sequence[str],
        *,
        initial_trials: int = 100,
        confirm_trials: int = 1000,
        min_joint_failure: float = 0.20,
        min_jri: float = 0.15,
        confidence_threshold: float = 0.95,
        posterior_samples: int = 10_000,
        seed: int = 20260810,
    ) -> None:
        if initial_trials <= 0:
            raise ValueError("initial_trials must be positive")

        if confirm_trials < initial_trials:
            raise ValueError("confirm_trials must be >= initial_trials")

        if not 0.0 < confidence_threshold < 1.0:
            raise ValueError("confidence_threshold must be between 0 and 1")

        self.invoke = invoke
        self.capabilities = tuple(sorted(set(capabilities)))
        self.initial_trials = initial_trials
        self.confirm_trials = confirm_trials
        self.min_joint_failure = min_joint_failure
        self.min_jri = min_jri
        self.confidence_threshold = confidence_threshold
        self.posterior_samples = posterior_samples
        self.rng = np.random.default_rng(seed)

    def _run_trials(
        self,
        configuration: tuple[str, ...],
        trials: int,
    ) -> TrialStats:
        active = set(configuration)

        failures = sum(not self.invoke(active).success for _ in range(trials))

        return TrialStats(
            trials=trials,
            failures=failures,
        )

    def _extend_trials(
        self,
        configuration: tuple[str, ...],
        current: TrialStats,
        target_trials: int,
    ) -> TrialStats:
        extra_trials = target_trials - current.trials

        if extra_trials <= 0:
            return current

        extra = self._run_trials(
            configuration,
            extra_trials,
        )

        return TrialStats(
            trials=current.trials + extra.trials,
            failures=current.failures + extra.failures,
        )

    def _posterior_samples(
        self,
        stats: TrialStats,
    ) -> np.ndarray:
        return self.rng.beta(
            stats.failures + 0.5,
            stats.trials - stats.failures + 0.5,
            size=self.posterior_samples,
        )

    def _interaction_confidence(
        self,
        pair: tuple[str, str],
        stats: dict[tuple[str, ...], TrialStats],
    ) -> float:
        first = (pair[0],)
        second = (pair[1],)

        joint_samples = self._posterior_samples(stats[pair])

        baseline_samples = self._posterior_samples(stats[()])

        first_samples = self._posterior_samples(stats[first])

        second_samples = self._posterior_samples(stats[second])

        max_subset_samples = np.maximum.reduce(
            [
                baseline_samples,
                first_samples,
                second_samples,
            ]
        )

        jri_samples = joint_samples - max_subset_samples

        valid = (joint_samples >= self.min_joint_failure) & (
            jri_samples >= self.min_jri
        )

        return float(np.mean(valid))

    def discover(self) -> SCIFReport:
        stats: dict[tuple[str, ...], TrialStats] = {}
        executions = 0

        stats[()] = self._run_trials(
            (),
            self.initial_trials,
        )
        executions += self.initial_trials

        for capability in self.capabilities:
            configuration = (capability,)

            stats[configuration] = self._run_trials(
                configuration,
                self.initial_trials,
            )

            executions += self.initial_trials

        suspicious_pairs: list[tuple[str, str]] = []

        for pair in combinations(self.capabilities, 2):
            stats[pair] = self._run_trials(
                pair,
                self.initial_trials,
            )

            executions += self.initial_trials

            subset_rate = max(
                stats[()].failure_rate,
                stats[(pair[0],)].failure_rate,
                stats[(pair[1],)].failure_rate,
            )

            joint_rate = stats[pair].failure_rate
            jri = joint_rate - subset_rate

            screening_joint_threshold = self.min_joint_failure * 0.75

            screening_jri_threshold = self.min_jri * 0.67

            if (
                joint_rate >= screening_joint_threshold
                and jri >= screening_jri_threshold
            ):
                suspicious_pairs.append(pair)

        candidates: list[SCIFCandidate] = []

        for pair in suspicious_pairs:
            current = stats[pair]

            confirmed = self._extend_trials(
                pair,
                current,
                self.confirm_trials,
            )

            executions += confirmed.trials - current.trials

            stats[pair] = confirmed

            max_subset_rate = max(
                stats[()].failure_rate,
                stats[(pair[0],)].failure_rate,
                stats[(pair[1],)].failure_rate,
            )

            joint_rate = confirmed.failure_rate
            jri = joint_rate - max_subset_rate

            confidence = self._interaction_confidence(
                pair,
                stats,
            )

            if (
                joint_rate >= self.min_joint_failure
                and jri >= self.min_jri
                and confidence >= self.confidence_threshold
            ):
                candidates.append(
                    SCIFCandidate(
                        capabilities=pair,
                        joint_failure_rate=joint_rate,
                        max_subset_failure_rate=max_subset_rate,
                        joint_risk_increment=jri,
                        confidence=confidence,
                    )
                )

        candidates.sort(
            key=lambda candidate: (
                -candidate.confidence,
                -candidate.joint_risk_increment,
                candidate.capabilities,
            )
        )

        return SCIFReport(
            stats=stats,
            candidates=tuple(candidates),
            executions=executions,
        )
