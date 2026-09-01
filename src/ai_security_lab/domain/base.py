"""Shared foundations for the AI Security Engineering Lab domain model."""

from typing import Literal

from pydantic import BaseModel, ConfigDict


SchemaVersion = Literal["1.0.0"]


class ContractModel(BaseModel):
    """Base class for validated domain objects."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
    )


class VersionedModel(ContractModel):
    """Base class for top-level objects governed by the evaluation contract."""

    schema_version: SchemaVersion = "1.0.0"