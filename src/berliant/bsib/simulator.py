from dataclasses import dataclass

import numpy as np

from berliant.bsib.scenario import FailureClass, Scenario


@dataclass(frozen=True)
class ExecutionResult:
    success: bool
    failure_class: FailureClass | None
    active_capabilities: frozenset[str]


class Simulator:
    """
    Legacy sequential synthetic simulator.

    The simulator internally knows the ground-truth failure
    probabilities, but invoke() exposes only observable outcomes.
    """

    def __init__(
        self,
        scenario: Scenario,
        seed: int = 42,
    ) -> None:
        self.scenario = scenario
        self.rng = np.random.default_rng(seed)

    def invoke(
        self,
        capabilities: set[str] | frozenset[str],
    ) -> ExecutionResult:
        active = frozenset(capabilities)

        unknown = active.difference(self.scenario.capabilities)

        if unknown:
            raise ValueError(f"Unknown capabilities: {sorted(unknown)}")

        failure_probability = self.scenario.baseline_failure

        failure_class = FailureClass.BASELINE_FAILURE

        for fault in self.scenario.faults:
            required = frozenset(fault.capabilities)

            if (
                required.issubset(active)
                and fault.failure_probability > failure_probability
            ):
                failure_probability = fault.failure_probability

                failure_class = fault.failure_class

        failed = bool(self.rng.random() < failure_probability)

        return ExecutionResult(
            success=not failed,
            failure_class=(failure_class if failed else None),
            active_capabilities=active,
        )
