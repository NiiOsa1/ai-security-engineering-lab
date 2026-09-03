"""Target domain model."""

from typing import Literal

from .base import VersionedModel


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

    target_id: str
    name: str
    target_type: TargetType