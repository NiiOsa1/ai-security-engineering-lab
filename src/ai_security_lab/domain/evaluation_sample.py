"""Evaluation Sample domain model."""

from typing import Annotated

from pydantic import StringConstraints

from .base import VersionedModel


SampleId = Annotated[
    str,
    StringConstraints(
        min_length=3,
        max_length=128,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    ),
]


SampleVersion = Annotated[
    str,
    StringConstraints(
        min_length=1,
    ),
]


ContentHash = Annotated[
    str,
    StringConstraints(
        pattern=r"^sha256:[0-9a-f]{64}$",
    ),
]


class EvaluationSample(VersionedModel):
    """The exact material supplied to an evaluation execution."""

    sample_id: SampleId
    version: SampleVersion
    content_hash: ContentHash