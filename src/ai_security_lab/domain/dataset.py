"""Dataset domain model."""

from typing import Annotated, Literal

from pydantic import StringConstraints

from .base import VersionedModel


DatasetId = Annotated[
    str,
    StringConstraints(
        min_length=3,
        max_length=128,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    ),
]


DatasetVersion = Annotated[
    str,
    StringConstraints(
        min_length=1,
    ),
]


DatasetProvenanceClass = Literal[
    "first-party-observed",
    "production-derived-sanitized",
    "real-world-public",
    "research-corpus",
    "lab-generated-empirical",
    "adversarially-generated",
    "synthetic",
    "deterministic-fixture",
]


class Dataset(VersionedModel):
    """A versioned collection of material available for evaluation."""

    dataset_id: DatasetId
    version: DatasetVersion
    provenance_class: DatasetProvenanceClass