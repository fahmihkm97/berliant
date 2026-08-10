from enum import StrEnum
from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class FailureClass(StrEnum):
    BASELINE_FAILURE = "BASELINE_FAILURE"
    CAPABILITY_SUPPRESSED = "CAPABILITY_SUPPRESSED"


class InteractionFault(BaseModel):
    id: str
    capabilities: tuple[str, ...]
    failure_probability: float = Field(ge=0.0, le=1.0)
    failure_class: FailureClass


class Scenario(BaseModel):
    id: str
    capabilities: tuple[str, ...]
    baseline_failure: float = Field(ge=0.0, le=1.0)
    faults: tuple[InteractionFault, ...] = ()


def load_scenario(path: str | Path) -> Scenario:
    scenario_path = Path(path)

    with scenario_path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return Scenario.model_validate(data)
