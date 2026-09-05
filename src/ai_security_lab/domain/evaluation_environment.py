"""Evaluation Environment domain model."""

from typing import Annotated, Literal, Self

from pydantic import Field, StringConstraints, model_validator

from .base import ContractModel, VersionedModel
from .control import ControlId, ControlVersion


EnvironmentId = Annotated[
    str,
    StringConstraints(
        min_length=3,
        max_length=128,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    ),
]


EnvironmentVersion = Annotated[
    str,
    StringConstraints(
        min_length=1,
    ),
]


ControlState = Literal[
    "enabled",
    "disabled",
    "observe-only",
    "not-applicable",
]


class EnvironmentControl(ContractModel):
    """A Control and its runtime state within an Evaluation Environment."""

    control_id: ControlId
    control_version: ControlVersion
    state: ControlState


class EvaluationEnvironment(VersionedModel):
    """Security-relevant runtime conditions for an evaluation."""

    environment_id: EnvironmentId
    version: EnvironmentVersion
    controls: list[EnvironmentControl] = Field(default_factory=list)

    @model_validator(mode="after")
    def reject_duplicate_control_ids(self) -> Self:
        control_ids = [control.control_id for control in self.controls]

        if len(control_ids) != len(set(control_ids)):
            raise ValueError(
                "control_id values must be unique within an evaluation environment"
            )

        return self