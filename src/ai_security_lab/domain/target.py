"""Target domain model."""

from typing import Annotated, Literal

from pydantic import StringConstraints

from .base import VersionedModel


TargetId = Annotated[
    str,
    StringConstraints(
        min_length=3,
        max_length=128,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    ),
]


TargetName = Annotated[
    str,
    StringConstraints(
        min_length=1,
    ),
]


TargetVersion = Annotated[
    str,
    StringConstraints(
        min_length=1,
    ),
]


TargetType = Literal[
    "llm",
    "agent",
    "rag",
    "voice",
    "mcp",
    "coding-agent",
]


class Target(VersionedModel):
    """A system or component being evaluated."""

    target_id: TargetId
    name: TargetName
    target_type: TargetType
    version: TargetVersion