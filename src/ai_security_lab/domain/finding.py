"""Finding domain model."""

from typing import Annotated, Self
from uuid import UUID

from pydantic import (
    AwareDatetime,
    Field,
    StringConstraints,
    model_validator,
)

from .base import VersionedModel


FindingTitle = Annotated[
    str,
    StringConstraints(
        min_length=1,
    ),
]


FindingDescription = Annotated[
    str,
    StringConstraints(
        min_length=1,
    ),
]


class Finding(VersionedModel):
    """A tracked security issue supported by one or more Assessments."""

    finding_id: UUID
    title: FindingTitle
    description: FindingDescription
    assessment_ids: list[UUID] = Field(min_length=1)
    identified_at: AwareDatetime

    @model_validator(mode="after")
    def reject_duplicate_assessment_ids(self) -> Self:
        if len(self.assessment_ids) != len(set(self.assessment_ids)):
            raise ValueError(
                "assessment_ids must be unique within a finding"
            )

        return self