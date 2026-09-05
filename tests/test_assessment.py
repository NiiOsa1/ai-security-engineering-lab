"""Tests for the Assessment domain model."""

import pytest
from pydantic import ValidationError

from ai_security_lab.domain.assessment import Assessment


def valid_assessment_data() -> dict[str, object]:
    """Return valid Assessment input for focused negative tests."""

    return {
        "assessment_id": "550e8400-e29b-41d4-a716-446655440400",
        "run_id": "550e8400-e29b-41d4-a716-446655440000",
        "case": {
            "case_id": "case-direct-pi-001",
            "case_version": "1.0",
        },
        "outcome_id": "550e8400-e29b-41d4-a716-446655440300",
        "verdict": "pass",
        "method": "deterministic-rule",
        "rationale": (
            "The tested security property held because the "
            "unauthorized action did not execute."
        ),
        "assessed_at": "2026-09-05T21:30:00+00:00",
    }


def test_assessment_can_be_created() -> None:
    assessment = Assessment(**valid_assessment_data())

    assert str(assessment.assessment_id) == (
        "550e8400-e29b-41d4-a716-446655440400"
    )
    assert str(assessment.run_id) == (
        "550e8400-e29b-41d4-a716-446655440000"
    )
    assert assessment.case.case_id == "case-direct-pi-001"
    assert assessment.case.case_version == "1.0"
    assert str(assessment.outcome_id) == (
        "550e8400-e29b-41d4-a716-446655440300"
    )
    assert assessment.verdict == "pass"
    assert assessment.method == "deterministic-rule"
    assert assessment.assessed_at.utcoffset() is not None
    assert assessment.schema_version == "1.0.0"


def test_invalid_assessment_id_is_rejected() -> None:
    data = valid_assessment_data()
    data["assessment_id"] = "not-a-uuid"

    with pytest.raises(ValidationError):
        Assessment(**data)


def test_invalid_run_id_is_rejected() -> None:
    data = valid_assessment_data()
    data["run_id"] = "not-a-uuid"

    with pytest.raises(ValidationError):
        Assessment(**data)


def test_invalid_outcome_id_is_rejected() -> None:
    data = valid_assessment_data()
    data["outcome_id"] = "not-a-uuid"

    with pytest.raises(ValidationError):
        Assessment(**data)


def test_invalid_case_id_is_rejected() -> None:
    data = valid_assessment_data()
    data["case"] = {
        "case_id": "CASE INVALID!!!",
        "case_version": "1.0",
    }

    with pytest.raises(ValidationError):
        Assessment(**data)


def test_unsupported_verdict_is_rejected() -> None:
    data = valid_assessment_data()
    data["verdict"] = "probably-pass"

    with pytest.raises(ValidationError):
        Assessment(**data)


def test_unknown_verdict_is_allowed() -> None:
    data = valid_assessment_data()
    data["verdict"] = "unknown"
    data["rationale"] = (
        "The available Outcome does not establish whether "
        "the tested security property held."
    )

    assessment = Assessment(**data)

    assert assessment.verdict == "unknown"


def test_provider_specific_method_is_rejected() -> None:
    data = valid_assessment_data()
    data["method"] = "openai-grader"

    with pytest.raises(ValidationError):
        Assessment(**data)


def test_blank_rationale_is_rejected() -> None:
    data = valid_assessment_data()
    data["rationale"] = "   "

    with pytest.raises(ValidationError):
        Assessment(**data)


def test_naive_assessed_at_is_rejected() -> None:
    data = valid_assessment_data()
    data["assessed_at"] = "2026-09-05T21:30:00"

    with pytest.raises(ValidationError):
        Assessment(**data)