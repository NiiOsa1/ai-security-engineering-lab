"""Outcome domain model."""

from typing import Literal, Self
from uuid import UUID

from pydantic import Field, model_validator

from .base import ContractModel, VersionedModel


FactState = Literal[
    "yes",
    "no",
    "unknown",
    "not-applicable",
]


class OutcomeFact(ContractModel):
    """One evidence-backed factual state observed during a Run."""

    state: FactState
    evidence_ids: list[UUID] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_evidence_support(self) -> Self:
        if (
            self.state in {"yes", "no"}
            and len(self.evidence_ids) == 0
        ):
            raise ValueError(
                "known fact states 'yes' and 'no' "
                "require at least one evidence_id"
            )

        if len(self.evidence_ids) != len(set(self.evidence_ids)):
            raise ValueError(
                "evidence_ids must be unique within an outcome fact"
            )

        return self


class Outcome(VersionedModel):
    """Evidence-backed factual states established for one evaluation Run."""

    outcome_id: UUID
    run_id: UUID

    action_proposed: OutcomeFact
    authorization_granted: OutcomeFact
    execution_attempted: OutcomeFact
    execution_occurred: OutcomeFact
    external_effect_occurred: OutcomeFact
    detection_occurred: OutcomeFact
    containment_occurred: OutcomeFact
    recovery_occurred: OutcomeFact