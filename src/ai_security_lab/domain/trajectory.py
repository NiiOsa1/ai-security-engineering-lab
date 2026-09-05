"""Trajectory domain model."""

from typing import Literal, Self
from uuid import UUID

from pydantic import AwareDatetime, Field, model_validator

from .base import ContractModel, VersionedModel


TrajectoryEventType = Literal[
    "input-received",
    "retrieval",
    "model-invocation",
    "model-output",
    "action-proposed",
    "authorization-decision",
    "execution-attempt",
    "execution-result",
    "external-effect-observed",
    "detection",
    "containment",
    "recovery",
    "output-produced",
    "error",
]


class TrajectoryEvent(ContractModel):
    """One externally observable event recorded during a Run."""

    event_id: UUID
    recorded_sequence: int = Field(ge=1)
    event_type: TrajectoryEventType
    occurred_at: AwareDatetime


class Trajectory(VersionedModel):
    """The externally observable event sequence recorded for one Run."""

    trajectory_id: UUID
    run_id: UUID
    events: list[TrajectoryEvent]

    @model_validator(mode="after")
    def validate_event_sequence(self) -> Self:
        event_ids = [event.event_id for event in self.events]

        if len(event_ids) != len(set(event_ids)):
            raise ValueError(
                "event_id values must be unique within a trajectory"
            )

        actual_sequence = [
            event.recorded_sequence for event in self.events
        ]
        expected_sequence = list(range(1, len(self.events) + 1))

        if actual_sequence != expected_sequence:
            raise ValueError(
                "recorded_sequence values must start at 1, "
                "be contiguous, and match recorded event order"
            )

        return self