"""Berliant public API.

Berliant provides stochastic capability-interaction discovery and
benchmark simulation utilities.
"""

from collections.abc import Sequence

from berliant.bsib import (
    ExecutionResult,
    FailureClass,
    InteractionFault,
    KeyedSimulator,
    Scenario,
    Simulator,
    load_scenario,
)
from berliant.discovery.scif import InvokeFunction
from berliant.discovery.scif_v4 import (
    ResidualRiskReport,
    SCIFDiscoveryV4,
    SCIFV4Report,
)

__version__ = "0.1.0"

# Stable user-facing alias for the current SCIF implementation.
SCIF = SCIFDiscoveryV4


def validated_scif(
    invoke: InvokeFunction,
    capabilities: Sequence[str],
    *,
    initial_trials: int = 100,
    screening_retest_trials: int = 300,
    screening_probability_threshold: float = 0.20,
    confirm_trials: int = 1500,
    subset_confirm_trials: int = 1000,
    min_joint_failure: float = 0.15,
    min_jri: float = 0.10,
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
) -> SCIFDiscoveryV4:
    """Create SCIF using the configuration validated in experiments."""
    return SCIFDiscoveryV4(
        invoke=invoke,
        capabilities=capabilities,
        initial_trials=initial_trials,
        screening_retest_trials=screening_retest_trials,
        screening_probability_threshold=screening_probability_threshold,
        confirm_trials=confirm_trials,
        subset_confirm_trials=subset_confirm_trials,
        min_joint_failure=min_joint_failure,
        min_jri=min_jri,
        confidence_threshold=confidence_threshold,
        posterior_samples=posterior_samples,
        residual_trials=residual_trials,
        min_residual_failure=min_residual_failure,
        min_residual_increment=min_residual_increment,
        higher_order_trials=higher_order_trials,
        higher_order_min_failure=higher_order_min_failure,
        higher_order_min_removal_drop=higher_order_min_removal_drop,
        higher_order_min_candidate_size=higher_order_min_candidate_size,
        seed=seed,
    )


__all__ = [
    "SCIF",
    "ExecutionResult",
    "FailureClass",
    "InteractionFault",
    "KeyedSimulator",
    "ResidualRiskReport",
    "SCIFDiscoveryV4",
    "SCIFV4Report",
    "Scenario",
    "Simulator",
    "load_scenario",
    "validated_scif",
]
