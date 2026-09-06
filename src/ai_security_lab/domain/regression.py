"""Regression domain model."""

from typing import Literal
from uuid import UUID

from pydantic import AwareDatetime

from .base import ContractModel, VersionedModel
from .case import CaseId, CaseVersion
from .evaluation_sample import SampleId, SampleVersion


class RegressionCase(ContractModel):
    """The exact Case promoted into permanent regression coverage."""

    case_id: CaseId
    case_version: CaseVersion


class RegressionSample(ContractModel):
    """The exact Evaluation Sample preserved for regression execution."""

    sample_id: SampleId
    sample_version: SampleVersion


class Regression(VersionedModel):
    """Permanent executable protection against recurrence of a security failure."""

    regression_id: UUID
    source_finding_id: UUID
    source_retest_id: UUID
    case: RegressionCase
    sample: RegressionSample
    required_verdict: Literal["pass"] = "pass"
    registered_at: AwareDatetime