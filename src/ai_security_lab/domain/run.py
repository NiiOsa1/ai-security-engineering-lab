"""Run domain model."""

import re
from typing import Annotated, Literal, Self
from uuid import UUID

from pydantic import AwareDatetime, StringConstraints, model_validator

from .base import ContractModel, VersionedModel
from .campaign import CampaignId, CampaignVersion
from .case import CaseId, CaseVersion
from .evaluation_environment import EnvironmentId, EnvironmentVersion
from .evaluation_sample import SampleId, SampleVersion
from .target import TargetId, TargetVersion


ProvenanceValue = Annotated[
    str,
    StringConstraints(
        min_length=1,
    ),
]


ExecutionProvenanceKind = Literal[
    "git-commit",
    "package-version",
    "oci-digest",
    "artifact-digest",
]


GIT_OBJECT_ID_PATTERN = re.compile(
    r"(?:[0-9a-f]{40}|[0-9a-f]{64})"
)

SHA256_DIGEST_PATTERN = re.compile(
    r"sha256:[0-9a-f]{64}"
)


class RunCampaign(ContractModel):
    """The exact Campaign version associated with a Run."""

    campaign_id: CampaignId
    campaign_version: CampaignVersion


class RunTarget(ContractModel):
    """The exact Target version used by a Run."""

    target_id: TargetId
    target_version: TargetVersion


class RunEnvironment(ContractModel):
    """The exact Evaluation Environment version used by a Run."""

    environment_id: EnvironmentId
    environment_version: EnvironmentVersion


class RunCase(ContractModel):
    """The exact Case version executed by a Run."""

    case_id: CaseId
    case_version: CaseVersion


class RunSample(ContractModel):
    """The exact Evaluation Sample version supplied to a Run."""

    sample_id: SampleId
    sample_version: SampleVersion


class ExecutionProvenanceReference(ContractModel):
    """A reference identifying software or an artifact used to execute a Run."""

    kind: ExecutionProvenanceKind
    value: ProvenanceValue

    @model_validator(mode="after")
    def validate_value_for_kind(self) -> Self:
        if self.kind == "git-commit":
            if GIT_OBJECT_ID_PATTERN.fullmatch(self.value) is None:
                raise ValueError(
                    "git-commit provenance must be a full "
                    "40- or 64-character hexadecimal Git object ID"
                )

        if self.kind in {"oci-digest", "artifact-digest"}:
            if SHA256_DIGEST_PATTERN.fullmatch(self.value) is None:
                raise ValueError(
                    f"{self.kind} provenance must use the format "
                    "sha256:<64 lowercase hexadecimal characters>"
                )

        return self


class Run(VersionedModel):
    """One exact historical evaluation execution."""

    run_id: UUID
    campaign: RunCampaign
    target: RunTarget
    environment: RunEnvironment
    case: RunCase
    sample: RunSample
    started_at: AwareDatetime
    execution_provenance: ExecutionProvenanceReference