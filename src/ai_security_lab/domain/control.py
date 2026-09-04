"""Control domain model."""

from typing import Annotated, Literal

from pydantic import StringConstraints

from .base import VersionedModel


ControlId = Annotated[
    str,
    StringConstraints(
        min_length=3,
        max_length=128,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    ),
]


ControlName = Annotated[
    str,
    StringConstraints(
        min_length=1,
    ),
]


ControlVersion = Annotated[
    str,
    StringConstraints(
        min_length=1,
    ),
]


ControlClass = Literal[
    "preventive",
    "restrictive",
    "detective",
    "containment",
    "recovery",
]


class Control(VersionedModel):
    """A versioned security mechanism used during evaluation."""

    control_id: ControlId
    name: ControlName
    version: ControlVersion
    control_classes: list[ControlClass] | None = None