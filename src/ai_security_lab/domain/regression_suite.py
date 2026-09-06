"""Regression Suite domain model."""

from typing import Annotated, Self
from uuid import UUID

from pydantic import Field, StringConstraints, model_validator

from .base import VersionedModel


RegressionSuiteId = Annotated[
    str,
    StringConstraints(
        min_length=3,
        max_length=128,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    ),
]


RegressionSuiteVersion = Annotated[
    str,
    StringConstraints(
        min_length=1,
    ),
]


class RegressionSuite(VersionedModel):
    """A versioned collection of permanent security regression obligations."""

    suite_id: RegressionSuiteId
    version: RegressionSuiteVersion
    regression_ids: list[UUID] = Field(min_length=1)

    @model_validator(mode="after")
    def reject_duplicate_regression_ids(self) -> Self:
        if len(self.regression_ids) != len(set(self.regression_ids)):
            raise ValueError(
                "regression_ids must be unique within a regression suite"
            )

        return self