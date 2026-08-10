from collections.abc import Sequence
from itertools import combinations

from berliant.discovery.scif import (
    InvokeFunction,
    SCIFCandidate,
    SCIFDiscovery,
    SCIFReport,
    TrialStats,
)


class SCIFDiscoveryV2(SCIFDiscovery):
    """
    SCIF v0.0.2.

    Pairwise screening remains inexpensive.

    When a pair becomes suspicious, confirmation re-estimates:
    - baseline
    - first singleton
    - second singleton
    - joint pair

    This reduces uncertainty in the subset estimates used by JRI.
    """

    def __init__(
        self,
        invoke: InvokeFunction,
        capabilities: Sequence[str],
        *,
        initial_trials: int = 100,
        confirm_trials: int = 1000,
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
            min_joint_failure=min_joint_failure,
            min_jri=min_jri,
            confidence_threshold=confidence_threshold,
            posterior_samples=posterior_samples,
            seed=seed,
        )

        if subset_confirm_trials < self.initial_trials:
            raise ValueError("subset_confirm_trials must be >= initial_trials")

        self.subset_confirm_trials = subset_confirm_trials

    def discover(self) -> SCIFReport:
        stats: dict[tuple[str, ...], TrialStats] = {}
        executions = 0

        # Stage 1: inexpensive baseline estimate.
        stats[()] = self._run_trials(
            (),
            self.initial_trials,
        )
        executions += self.initial_trials

        # Stage 1: inexpensive singleton estimates.
        for capability in self.capabilities:
            configuration = (capability,)

            stats[configuration] = self._run_trials(
                configuration,
                self.initial_trials,
            )

            executions += self.initial_trials

        suspicious_pairs: list[tuple[str, str]] = []

        # Stage 1: inexpensive pairwise screening.
        for raw_pair in combinations(
            self.capabilities,
            2,
        ):
            pair = (
                raw_pair[0],
                raw_pair[1],
            )

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

        # Stage 2: balanced confirmation.
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
