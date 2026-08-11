from collections.abc import Sequence
from dataclasses import dataclass

from berliant.discovery.scif import InvokeFunction


@dataclass(frozen=True)
class HigherOrderLocalizationReport:
    source_configuration: tuple[str, ...]
    source_failure_rate: float
    removal_rates: dict[str, float]
    candidate: tuple[str, ...] | None
    candidate_failure_rate: float | None
    immediate_subset_rates: dict[
        tuple[str, ...],
        float,
    ]
    executions: int


class ResidualHigherOrderLocalizer:
    """
    Localize higher-order interactions inside a residual
    configuration.

    The input configuration is assumed to have known pairwise
    interactions already disabled by the SCIF V4 residual-risk
    stage.

    This prevents known pairwise faults from masking
    higher-order deletion signals.
    """

    def __init__(
        self,
        invoke: InvokeFunction,
        *,
        trials_per_config: int = 1000,
        min_failure: float = 0.15,
        min_removal_drop: float = 0.10,
        min_candidate_size: int = 3,
    ) -> None:
        if trials_per_config <= 0:
            raise ValueError("trials_per_config must be positive")

        if min_candidate_size < 3:
            raise ValueError("min_candidate_size must be at least 3")

        if not 0.0 <= min_failure <= 1.0:
            raise ValueError("min_failure must be between 0 and 1")

        if not 0.0 <= min_removal_drop <= 1.0:
            raise ValueError("min_removal_drop must be between 0 and 1")

        self.invoke = invoke
        self.trials_per_config = trials_per_config
        self.min_failure = min_failure
        self.min_removal_drop = min_removal_drop
        self.min_candidate_size = min_candidate_size

    def _estimate_failure_rate(
        self,
        configuration: tuple[str, ...],
    ) -> float:
        active = set(configuration)

        failures = sum(
            not self.invoke(active).success for _ in range(self.trials_per_config)
        )

        return failures / self.trials_per_config

    def localize(
        self,
        configuration: Sequence[str],
    ) -> HigherOrderLocalizationReport:
        source_configuration = tuple(sorted(set(configuration)))

        source_failure_rate = self._estimate_failure_rate(source_configuration)

        executions = self.trials_per_config

        removal_rates: dict[
            str,
            float,
        ] = {}

        essential: list[str] = []

        for capability in source_configuration:
            reduced = tuple(item for item in source_configuration if item != capability)

            removal_rate = self._estimate_failure_rate(reduced)

            executions += self.trials_per_config

            removal_rates[capability] = removal_rate

            removal_drop = source_failure_rate - removal_rate

            if (
                source_failure_rate >= self.min_failure
                and removal_drop >= self.min_removal_drop
            ):
                essential.append(capability)

        if len(essential) < self.min_candidate_size:
            return HigherOrderLocalizationReport(
                source_configuration=(source_configuration),
                source_failure_rate=(source_failure_rate),
                removal_rates=removal_rates,
                candidate=None,
                candidate_failure_rate=None,
                immediate_subset_rates={},
                executions=executions,
            )

        candidate = tuple(sorted(essential))

        candidate_failure_rate = self._estimate_failure_rate(candidate)

        executions += self.trials_per_config

        immediate_subset_rates: dict[
            tuple[str, ...],
            float,
        ] = {}

        for capability in candidate:
            subset = tuple(item for item in candidate if item != capability)

            subset_rate = self._estimate_failure_rate(subset)

            executions += self.trials_per_config

            immediate_subset_rates[subset] = subset_rate

        max_subset_rate = max(immediate_subset_rates.values())

        final_candidate: tuple[str, ...] | None = candidate

        if (
            candidate_failure_rate < self.min_failure
            or candidate_failure_rate - max_subset_rate < self.min_removal_drop
        ):
            final_candidate = None

        return HigherOrderLocalizationReport(
            source_configuration=(source_configuration),
            source_failure_rate=(source_failure_rate),
            removal_rates=removal_rates,
            candidate=final_candidate,
            candidate_failure_rate=(candidate_failure_rate),
            immediate_subset_rates=(immediate_subset_rates),
            executions=executions,
        )
