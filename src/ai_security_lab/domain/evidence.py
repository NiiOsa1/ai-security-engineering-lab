"""Evidence domain model."""

from typing import Annotated, Literal, Self
from uuid import UUID

from pydantic import (
    AwareDatetime,
    Field,
    StringConstraints,
    model_validator,
)

from .base import ContractModel, VersionedModel


EvidenceSourceId = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=128,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    ),
]


ArtifactDigest = Annotated[
    str,
    StringConstraints(
        pattern=r"^sha256:[0-9a-f]{64}$",
    ),
]


MediaType = Annotated[
    str,
    StringConstraints(
        min_length=1,
    ),
]


EvidenceKind = Literal[
    "input-artifact",
    "model-output",
    "retrieval-record",
    "authorization-record",
    "execution-record",
    "external-state",
    "system-log",
    "network-observation",
    "detection-record",
    "containment-record",
    "recovery-record",
]


EvidenceSensitivity = Literal[
    "unknown",
    "non-sensitive",
    "sensitive",
]


class ArtifactReference(ContractModel):
    """A content-identified artifact associated with Evidence."""

    artifact_id: UUID
    content_hash: ArtifactDigest
    media_type: MediaType


class Evidence(VersionedModel):
    """An objective artifact reference collected during an evaluation Run."""

    evidence_id: UUID
    run_id: UUID
    related_event_ids: list[UUID] = Field(default_factory=list)
    evidence_kind: EvidenceKind
    source_component: EvidenceSourceId
    collected_at: AwareDatetime
    sensitivity: EvidenceSensitivity = "unknown"
    artifact: ArtifactReference

    @model_validator(mode="after")
    def reject_duplicate_related_event_ids(self) -> Self:
        if len(self.related_event_ids) != len(set(self.related_event_ids)):
            raise ValueError(
                "related_event_ids must be unique within an evidence record"
            )

        return self