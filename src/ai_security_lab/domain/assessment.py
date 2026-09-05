"""Assessment domain model."""

from typing import Annotated, Literal
from uuid import UUID

from pydantic import AwareDatetime, StringConstraints

from .base import ContractModel, VersionedModel
from .case import CaseId, CaseVersion


AssessmentVerdict = Literal[
    "pass",
    "fail",
    "unknown",
    "not-applicable",
]


AssessmentMethod = Literal[
    "deterministic-rule",
    "model-grader",
    "human-review",
]


AssessmentRationale = Annotated[
    str,
    StringConstraints(
        min_length=1,
    ),
]


class AssessmentCase(ContractModel):
    """The exact Case version interpreted by an Assessment."""

    case_id: CaseId
    case_version: CaseVersion


class Assessment(VersionedModel):
    """A security interpretation of an evidence-backed Outcome."""

    assessment_id: UUID
    run_id: UUID
    case: AssessmentCase
    outcome_id: UUID
    verdict: AssessmentVerdict
    method: AssessmentMethod
    rationale: AssessmentRationale
    assessed_at: AwareDatetime