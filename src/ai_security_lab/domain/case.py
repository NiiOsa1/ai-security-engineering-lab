"""Case domain model."""

from typing import Annotated

from pydantic import StringConstraints

from .base import VersionedModel


CaseId = Annotated[
    str,
    StringConstraints(
        min_length=3,
        max_length=128,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    ),
]


CaseVersion = Annotated[
    str,
    StringConstraints(
        min_length=1,
    ),
]


SecurityProperty = Annotated[
    str,
    StringConstraints(
        min_length=1,
    ),
]


FailureCondition = Annotated[
    str,
    StringConstraints(
        min_length=1,
    ),
]


class Case(VersionedModel):
    """A versioned security condition or property to be evaluated."""

    case_id: CaseId
    version: CaseVersion
    security_property: SecurityProperty
    failure_condition: FailureCondition