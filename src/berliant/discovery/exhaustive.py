from collections.abc import Callable, Sequence
from dataclasses import dataclass
from itertools import combinations

from berliant.bsib import ExecutionResult

InvokeFunction = Callable[[set[str]], ExecutionResult]


@dataclass(frozen=True)
class InteractionCandidate:
    capabilities: tuple[str, ...]
    joint_failure_rate: float
    max_subset_failure_rate: float
    joint_risk_increment: float


@dataclass(frozen=True)
class DiscoveryReport:
    rates: dict[tuple[str, ...], float]
    candidates: tuple[InteractionCandidate, ...]
    executions: int


class ExhaustiveDiscovery:
    """
    Exhaustively estimates capability configurations up to max_order.

    This baseline is intentionally simple and expensive. It provides
    a reference result that Berliant-SCIF must later match using fewer
    executions.
    """

    def __init__(
        self,
        invoke: InvokeFunction,
        capabilities: Sequence[str],
        *,
        max_order: int = 2,
        trials_per_config: int = 1000,
        min_joint_failure: float = 0.20,
        min_jri: float = 0.15,
    ) -> None:
        if max_order < 2:
            raise ValueError("max_order must be at least 2")

        if trials_per_config <= 0:
            raise ValueError("trials_per_config must be positive")

        self.invoke = invoke
        self.capabilities = tuple(sorted(set(capabilities)))
        self.max_order = min(max_order, len(self.capabilities))
        self.trials_per_config = trials_per_config
        self.min_joint_failure = min_joint_failure
        self.min_jri = min_jri

    def _estimate_failure_rate(
        self,
        configuration: tuple[str, ...],
    ) -> float:
        active = set(configuration)

        failures = sum(
            not self.invoke(active).success for _ in range(self.trials_per_config)
        )

        return failures / self.trials_per_config

    def discover(self) -> DiscoveryReport:
        rates: dict[tuple[str, ...], float] = {}
        executions = 0

        # Empty configuration gives us the synthetic baseline.
        rates[()] = self._estimate_failure_rate(())
        executions += self.trials_per_config

        # Measure every configuration up to max_order.
        for order in range(1, self.max_order + 1):
            for configuration in combinations(
                self.capabilities,
                order,
            ):
                rates[configuration] = self._estimate_failure_rate(configuration)
                executions += self.trials_per_config

        candidates: list[InteractionCandidate] = []

        for configuration, joint_rate in rates.items():
            if len(configuration) < 2:
                continue

            subset_rates: list[float] = []

            for subset_order in range(len(configuration)):
                for subset in combinations(
                    configuration,
                    subset_order,
                ):
                    subset_rates.append(rates[subset])

            max_subset_rate = max(subset_rates)
            jri = joint_rate - max_subset_rate

            if joint_rate >= self.min_joint_failure and jri >= self.min_jri:
                candidates.append(
                    InteractionCandidate(
                        capabilities=configuration,
                        joint_failure_rate=joint_rate,
                        max_subset_failure_rate=max_subset_rate,
                        joint_risk_increment=jri,
                    )
                )

        candidates.sort(
            key=lambda candidate: (
                -candidate.joint_risk_increment,
                -candidate.joint_failure_rate,
                candidate.capabilities,
            )
        )

        return DiscoveryReport(
            rates=rates,
            candidates=tuple(candidates),
            executions=executions,
        )
