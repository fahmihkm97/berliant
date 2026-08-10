from collections.abc import Callable, Sequence
from dataclasses import dataclass

from berliant.bsib import ExecutionResult

InvokeFunction = Callable[[set[str]], ExecutionResult]


@dataclass(frozen=True)
class DeletionReport:
    full_failure_rate: float
    removal_rates: dict[str, float]
    candidate: tuple[str, ...] | None
    candidate_failure_rate: float | None
    immediate_subset_rates: dict[
        tuple[str, ...],
        float,
    ]
    executions: int


class DeletionLocalizationBaseline:
    """
    Higher-order localization baseline.

    Assumptions:
    - one dominant interaction fault
    - monotonic activation
    - removing an essential capability reduces failure risk

    This is a benchmark baseline, not the SCIF algorithm.
    """

    def __init__(
        self,
        invoke: InvokeFunction,
        capabilities: Sequence[str],
        *,
        trials_per_config: int = 1000,
        min_failure: float = 0.20,
        min_removal_drop: float = 0.20,
        min_candidate_size: int = 2,
    ) -> None:
        if trials_per_config <= 0:
            raise ValueError("trials_per_config must be positive")

        if min_candidate_size < 2:
            raise ValueError("min_candidate_size must be at least 2")

        self.invoke = invoke
        self.capabilities = tuple(sorted(set(capabilities)))

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

    def discover(
        self,
    ) -> DeletionReport:
        full = self.capabilities

        full_failure_rate = self._estimate_failure_rate(full)

        executions = self.trials_per_config

        removal_rates: dict[
            str,
            float,
        ] = {}

        essential: list[str] = []

        for capability in full:
            reduced = tuple(item for item in full if item != capability)

            removal_rate = self._estimate_failure_rate(reduced)

            executions += self.trials_per_config

            removal_rates[capability] = removal_rate

            removal_drop = full_failure_rate - removal_rate

            if (
                full_failure_rate >= self.min_failure
                and removal_drop >= self.min_removal_drop
            ):
                essential.append(capability)

        if len(essential) < self.min_candidate_size:
            return DeletionReport(
                full_failure_rate=(full_failure_rate),
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

        return DeletionReport(
            full_failure_rate=(full_failure_rate),
            removal_rates=removal_rates,
            candidate=final_candidate,
            candidate_failure_rate=(candidate_failure_rate),
            immediate_subset_rates=(immediate_subset_rates),
            executions=executions,
        )
