"""Remediation domain model."""

from typing import Annotated, Self
from uuid import UUID

from pydantic import (
    AwareDatetime,
    Field,
    StringConstraints,
    model_validator,
)

from .base import VersionedModel


IntendedChange = Annotated[
    str,
    StringConstraints(
        min_length=1,
    ),
]


class Remediation(VersionedModel):
    """An intended corrective change for one or more Findings."""

    remediation_id: UUID
    finding_ids: list[UUID] = Field(min_length=1)
    intended_change: IntendedChange
    proposed_at: AwareDatetime

    @model_validator(mode="after")
    def reject_duplicate_finding_ids(self) -> Self:
        if len(self.finding_ids) != len(set(self.finding_ids)):
            raise ValueError(
                "finding_ids must be unique within a remediation"
            )

        return self