"""Campaign domain model."""

from typing import Annotated, Self

from pydantic import Field, StringConstraints, model_validator

from .base import ContractModel, VersionedModel
from .case import CaseId, CaseVersion
from .evaluation_environment import EnvironmentId, EnvironmentVersion
from .target import TargetId, TargetVersion


CampaignId = Annotated[
    str,
    StringConstraints(
        min_length=3,
        max_length=128,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    ),
]


CampaignVersion = Annotated[
    str,
    StringConstraints(
        min_length=1,
    ),
]


class CampaignTarget(ContractModel):
    """The exact Target version selected for a Campaign."""

    target_id: TargetId
    target_version: TargetVersion


class CampaignEnvironment(ContractModel):
    """The exact Evaluation Environment version selected for a Campaign."""

    environment_id: EnvironmentId
    environment_version: EnvironmentVersion


class CampaignCase(ContractModel):
    """The exact Case version selected for a Campaign."""

    case_id: CaseId
    case_version: CaseVersion


class Campaign(VersionedModel):
    """A controlled configuration for a collection of evaluation Runs."""

    campaign_id: CampaignId
    version: CampaignVersion
    target: CampaignTarget
    environment: CampaignEnvironment
    cases: list[CampaignCase] = Field(min_length=1)
    repetitions_per_case: int = Field(default=1, ge=1)

    @model_validator(mode="after")
    def reject_duplicate_case_ids(self) -> Self:
        case_ids = [case.case_id for case in self.cases]

        if len(case_ids) != len(set(case_ids)):
            raise ValueError(
                "case_id values must be unique within a campaign"
            )

        return self