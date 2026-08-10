import hashlib
import json
from dataclasses import dataclass, field

from berliant.bsib.scenario import (
    FailureClass,
    Scenario,
)
from berliant.bsib.simulator import ExecutionResult


@dataclass
class KeyedSimulator:
    """
    Order-independent synthetic simulator.

    Each capability configuration receives its own deterministic
    random stream. Therefore, the first N observations for a given
    configuration are identical regardless of how other
    configurations are interleaved.

    This is intended for controlled benchmark comparisons.
    """

    scenario: Scenario
    seed: int = 42

    _draw_counts: dict[
        frozenset[str],
        int,
    ] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    def _next_uniform(
        self,
        active: frozenset[str],
    ) -> float:
        draw_index = self._draw_counts.get(
            active,
            0,
        )

        self._draw_counts[active] = draw_index + 1

        configuration = json.dumps(
            sorted(active),
            separators=(",", ":"),
        )

        payload = (
            f"{self.scenario.id}|{self.seed}|{configuration}|{draw_index}"
        ).encode()

        digest = hashlib.blake2b(
            payload,
            digest_size=8,
        ).digest()

        integer = int.from_bytes(
            digest,
            byteorder="big",
            signed=False,
        )

        return integer / (1 << 64)

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

        failed = self._next_uniform(active) < failure_probability

        return ExecutionResult(
            success=not failed,
            failure_class=(failure_class if failed else None),
            active_capabilities=active,
        )
