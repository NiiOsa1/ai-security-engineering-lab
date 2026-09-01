"""Target domain model."""

from .base import VersionedModel


class Target(VersionedModel):
    """A system or component being evaluated."""

    target_id: str
    name: str
    target_type: str