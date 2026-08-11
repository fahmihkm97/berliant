from collections.abc import Sequence
from dataclasses import dataclass
from itertools import combinations

from berliant.discovery.residual_localization import (
    HigherOrderLocalizationReport,
    ResidualHigherOrderLocalizer,
)
from berliant.discovery.scif import (
    InvokeFunction,
    SCIFReport,
    TrialStats,
)
from berliant.discovery.scif_v3 import SCIFDiscoveryV3


@dataclass(frozen=True)
class ResidualRiskReport:
    baseline_failure_rate: float
    full_failure_rate: float
    probe_failure_rates: dict[
        tuple[str, ...],
        float,
    ]
    residual_failure_rate: float
    residual_risk_increment: float
    residual_detected: bool
    executions: int


@dataclass(frozen=True)
class SCIFV4Report:
    pairwise_report: SCIFReport
    residual: ResidualRiskReport
    higher_order: HigherOrderLocalizationReport | None
    executions: int


class SCIFDiscoveryV4:
    """
    SCIF v0.0.4.

    Pipeline:
    1. SCIF V3 pairwise discovery.
    2. Residual-risk detection after known pair suppression.
    3. Higher-order localization when residual risk remains.
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
        residual_trials: int = 1000,
        min_residual_failure: float = 0.15,
        min_residual_increment: float = 0.10,
        higher_order_trials: int = 1000,
        higher_order_min_failure: float = 0.15,
        higher_order_min_removal_drop: float = 0.10,
        higher_order_min_candidate_size: int = 3,
        seed: int = 20260810,
    ) -> None:
        if residual_trials <= 0:
            raise ValueError("residual_trials must be positive")

        if not 0.0 <= min_residual_failure <= 1.0:
            raise ValueError("min_residual_failure must be between 0 and 1")

        if not 0.0 <= min_residual_increment <= 1.0:
            raise ValueError("min_residual_increment must be between 0 and 1")

        self.invoke = invoke

        self.capabilities = tuple(sorted(set(capabilities)))

        self.residual_trials = residual_trials
        self.min_residual_failure = min_residual_failure
        self.min_residual_increment = min_residual_increment

        self.pairwise_discovery = SCIFDiscoveryV3(
            invoke=invoke,
            capabilities=self.capabilities,
            initial_trials=initial_trials,
            screening_retest_trials=(screening_retest_trials),
            screening_probability_threshold=(screening_probability_threshold),
            confirm_trials=confirm_trials,
            subset_confirm_trials=(subset_confirm_trials),
            min_joint_failure=min_joint_failure,
            min_jri=min_jri,
            confidence_threshold=(confidence_threshold),
            posterior_samples=posterior_samples,
            seed=seed,
        )

        self.higher_order_localizer = ResidualHigherOrderLocalizer(
            invoke=invoke,
            trials_per_config=(higher_order_trials),
            min_failure=(higher_order_min_failure),
            min_removal_drop=(higher_order_min_removal_drop),
            min_candidate_size=(higher_order_min_candidate_size),
        )

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

    def _minimal_hitting_sets(
        self,
        pairs: tuple[
            tuple[str, str],
            ...,
        ],
    ) -> tuple[
        tuple[str, ...],
        ...,
    ]:
        """
        Find inclusion-minimal capability-removal sets that
        disable every known pairwise interaction.
        """

        if not pairs:
            return ((),)

        hitting_sets: list[tuple[str, ...]] = []

        for size in range(
            1,
            len(self.capabilities) + 1,
        ):
            for raw_candidate in combinations(
                self.capabilities,
                size,
            ):
                candidate = tuple(raw_candidate)

                selected = frozenset(candidate)

                hits_every_pair = all(selected.intersection(pair) for pair in pairs)

                if not hits_every_pair:
                    continue

                has_smaller_hitting_set = any(
                    frozenset(existing).issubset(selected) for existing in hitting_sets
                )

                if has_smaller_hitting_set:
                    continue

                hitting_sets.append(candidate)

        return tuple(hitting_sets)

    def _probe_failure_rate(
        self,
        configuration: tuple[str, ...],
    ) -> float:
        stats = self._run_trials(
            configuration,
            self.residual_trials,
        )

        return stats.failure_rate

    def _residual_probe(
        self,
        pairwise_report: SCIFReport,
    ) -> ResidualRiskReport:
        baseline_failure_rate = pairwise_report.stats[()].failure_rate

        full_configuration = self.capabilities

        full_failure_rate = self._probe_failure_rate(full_configuration)

        executions = self.residual_trials

        known_pairs = tuple(
            candidate.capabilities for candidate in pairwise_report.candidates
        )

        removal_sets = self._minimal_hitting_sets(known_pairs)

        probe_failure_rates: dict[
            tuple[str, ...],
            float,
        ] = {}

        if not known_pairs:
            probe_failure_rates[()] = full_failure_rate

        else:
            for removal_set in removal_sets:
                removed = frozenset(removal_set)

                residual_configuration = tuple(
                    capability
                    for capability in self.capabilities
                    if capability not in removed
                )

                rate = self._probe_failure_rate(residual_configuration)

                executions += self.residual_trials

                probe_failure_rates[removal_set] = rate

        residual_failure_rate = max(probe_failure_rates.values())

        residual_risk_increment = residual_failure_rate - baseline_failure_rate

        residual_detected = (
            full_failure_rate >= self.min_residual_failure
            and residual_failure_rate >= self.min_residual_failure
            and residual_risk_increment >= self.min_residual_increment
        )

        return ResidualRiskReport(
            baseline_failure_rate=(baseline_failure_rate),
            full_failure_rate=(full_failure_rate),
            probe_failure_rates=(probe_failure_rates),
            residual_failure_rate=(residual_failure_rate),
            residual_risk_increment=(residual_risk_increment),
            residual_detected=(residual_detected),
            executions=executions,
        )

    def _localize_residual(
        self,
        residual_report: ResidualRiskReport,
    ) -> HigherOrderLocalizationReport | None:
        if not residual_report.residual_detected:
            return None

        probe_rates = residual_report.probe_failure_rates

        removal_set = max(
            probe_rates,
            key=lambda candidate: probe_rates[candidate],
        )

        removed = frozenset(removal_set)

        residual_configuration = tuple(
            capability for capability in self.capabilities if capability not in removed
        )

        return self.higher_order_localizer.localize(residual_configuration)

    def discover(
        self,
    ) -> SCIFV4Report:
        pairwise_report = self.pairwise_discovery.discover()

        residual_report = self._residual_probe(pairwise_report)

        higher_order_report = self._localize_residual(residual_report)

        higher_order_executions = 0

        if higher_order_report is not None:
            higher_order_executions = higher_order_report.executions

        total_executions = (
            pairwise_report.executions
            + residual_report.executions
            + higher_order_executions
        )

        return SCIFV4Report(
            pairwise_report=(pairwise_report),
            residual=(residual_report),
            higher_order=(higher_order_report),
            executions=(total_executions),
        )
