"""Retest domain model."""

from uuid import UUID

from .base import VersionedModel


class Retest(VersionedModel):
    """A post-remediation evaluation linked to a Finding."""

    retest_id: UUID
    finding_id: UUID
    remediation_id: UUID
    run_id: UUID
    assessment_id: UUID