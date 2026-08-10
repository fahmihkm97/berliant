from collections.abc import Sequence
from itertools import combinations

import numpy as np

from berliant.discovery.scif import (
    InvokeFunction,
    SCIFCandidate,
    SCIFReport,
    TrialStats,
)
from berliant.discovery.scif_v2 import SCIFDiscoveryV2


class SCIFDiscoveryV3(SCIFDiscoveryV2):
    """
    SCIF v0.0.3.

    Adds adaptive screening for borderline pairwise interactions.
    """

    def __init__(
        self,
        invoke: InvokeFunction,
        capabilities: Sequence[str],
        *,
        initial_trials: int = 100,
        screening_retest_trials: int = 300,
        screening_probability_threshold: float = 0.20,
        confirm_trials: int = 1500,
        subset_confirm_trials: int = 1000,
        min_joint_failure: float = 0.20,
        min_jri: float = 0.15,
        confidence_threshold: float = 0.95,
        posterior_samples: int = 10_000,
        seed: int = 20260810,
    ) -> None:
        super().__init__(
            invoke=invoke,
            capabilities=capabilities,
            initial_trials=initial_trials,
            confirm_trials=confirm_trials,
            subset_confirm_trials=subset_confirm_trials,
            min_joint_failure=min_joint_failure,
            min_jri=min_jri,
            confidence_threshold=confidence_threshold,
            posterior_samples=posterior_samples,
            seed=seed,
        )

        if screening_retest_trials < initial_trials:
            raise ValueError("screening_retest_trials must be >= initial_trials")

        if not 0.0 < screening_probability_threshold < 1.0:
            raise ValueError("screening_probability_threshold must be between 0 and 1")

        self.screening_retest_trials = screening_retest_trials
        self.screening_probability_threshold = screening_probability_threshold

    def _screening_thresholds(
        self,
    ) -> tuple[float, float]:
        joint_threshold = self.min_joint_failure * 0.75

        jri_threshold = self.min_jri * 0.67

        return (
            joint_threshold,
            jri_threshold,
        )

    def _screening_rates(
        self,
        pair: tuple[str, str],
        stats: dict[tuple[str, ...], TrialStats],
    ) -> tuple[float, float]:
        joint_rate = stats[pair].failure_rate

        max_subset_rate = max(
            stats[()].failure_rate,
            stats[(pair[0],)].failure_rate,
            stats[(pair[1],)].failure_rate,
        )

        return (
            joint_rate,
            joint_rate - max_subset_rate,
        )

    def _passes_screening(
        self,
        pair: tuple[str, str],
        stats: dict[tuple[str, ...], TrialStats],
    ) -> bool:
        joint_rate, jri = self._screening_rates(
            pair,
            stats,
        )

        joint_threshold, jri_threshold = self._screening_thresholds()

        return joint_rate >= joint_threshold and jri >= jri_threshold

    def _screening_probability(
        self,
        pair: tuple[str, str],
        stats: dict[tuple[str, ...], TrialStats],
    ) -> float:
        joint_samples = self._posterior_samples(stats[pair])

        baseline_samples = self._posterior_samples(stats[()])

        first_samples = self._posterior_samples(stats[(pair[0],)])

        second_samples = self._posterior_samples(stats[(pair[1],)])

        max_subset_samples = np.maximum.reduce(
            [
                baseline_samples,
                first_samples,
                second_samples,
            ]
        )

        jri_samples = joint_samples - max_subset_samples

        joint_threshold, jri_threshold = self._screening_thresholds()

        valid = (joint_samples >= joint_threshold) & (jri_samples >= jri_threshold)

        return float(np.mean(valid))

    def _extend_screening_context(
        self,
        pair: tuple[str, str],
        stats: dict[tuple[str, ...], TrialStats],
    ) -> int:
        added_executions = 0

        configurations: tuple[
            tuple[str, ...],
            ...,
        ] = (
            (),
            (pair[0],),
            (pair[1],),
            pair,
        )

        for config in configurations:
            current = stats[config]

            updated = self._extend_trials(
                config,
                current,
                self.screening_retest_trials,
            )

            added_executions += updated.trials - current.trials

            stats[config] = updated

        return added_executions

    def discover(self) -> SCIFReport:
        stats: dict[tuple[str, ...], TrialStats] = {}
        executions = 0

        stats[()] = self._run_trials(
            (),
            self.initial_trials,
        )

        executions += self.initial_trials

        for capability in self.capabilities:
            singleton_config = (capability,)

            stats[singleton_config] = self._run_trials(
                singleton_config,
                self.initial_trials,
            )

            executions += self.initial_trials

        pairs: list[tuple[str, str]] = []

        for raw_pair in combinations(
            self.capabilities,
            2,
        ):
            pair = (
                raw_pair[0],
                raw_pair[1],
            )

            pairs.append(pair)

            stats[pair] = self._run_trials(
                pair,
                self.initial_trials,
            )

            executions += self.initial_trials

        suspicious_pairs: list[tuple[str, str]] = []

        borderline_pairs: list[tuple[str, str]] = []

        joint_threshold, _ = self._screening_thresholds()

        for pair in pairs:
            if self._passes_screening(
                pair,
                stats,
            ):
                suspicious_pairs.append(pair)
                continue

            joint_rate = stats[pair].failure_rate

            if joint_rate < joint_threshold:
                continue

            probability = self._screening_probability(
                pair,
                stats,
            )

            if probability >= self.screening_probability_threshold:
                borderline_pairs.append(pair)

        for pair in borderline_pairs:
            executions += self._extend_screening_context(
                pair,
                stats,
            )

            if self._passes_screening(
                pair,
                stats,
            ):
                suspicious_pairs.append(pair)

        candidates: list[SCIFCandidate] = []

        for pair in suspicious_pairs:
            subset_configurations: tuple[
                tuple[str, ...],
                ...,
            ] = (
                (),
                (pair[0],),
                (pair[1],),
            )

            for subset_config in subset_configurations:
                current = stats[subset_config]

                updated = self._extend_trials(
                    subset_config,
                    current,
                    self.subset_confirm_trials,
                )

                executions += updated.trials - current.trials

                stats[subset_config] = updated

            current_pair = stats[pair]

            confirmed_pair = self._extend_trials(
                pair,
                current_pair,
                self.confirm_trials,
            )

            executions += confirmed_pair.trials - current_pair.trials

            stats[pair] = confirmed_pair

            max_subset_rate = max(
                stats[()].failure_rate,
                stats[(pair[0],)].failure_rate,
                stats[(pair[1],)].failure_rate,
            )

            joint_rate = confirmed_pair.failure_rate

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
                        max_subset_failure_rate=(max_subset_rate),
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
