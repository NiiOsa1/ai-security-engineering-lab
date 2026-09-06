"""Tests for the Regression domain model."""

import pytest
from pydantic import ValidationError

from ai_security_lab.domain.regression import Regression


def valid_regression_data() -> dict[str, object]:
    """Return valid Regression input for focused negative tests."""

    return {
        "regression_id": "550e8400-e29b-41d4-a716-446655440800",
        "source_finding_id": "550e8400-e29b-41d4-a716-446655440500",
        "source_retest_id": "550e8400-e29b-41d4-a716-446655440700",
        "case": {
            "case_id": "case-direct-pi-001",
            "case_version": "1.0",
        },
        "sample": {
            "sample_id": "sample-001",
            "sample_version": "1.0",
        },
        "required_verdict": "pass",
        "registered_at": "2026-09-06T02:00:00+00:00",
    }


def test_regression_can_be_created() -> None:
    regression = Regression(**valid_regression_data())

    assert str(regression.regression_id) == (
        "550e8400-e29b-41d4-a716-446655440800"
    )
    assert str(regression.source_finding_id) == (
        "550e8400-e29b-41d4-a716-446655440500"
    )
    assert str(regression.source_retest_id) == (
        "550e8400-e29b-41d4-a716-446655440700"
    )
    assert regression.case.case_id == "case-direct-pi-001"
    assert regression.case.case_version == "1.0"
    assert regression.sample.sample_id == "sample-001"
    assert regression.sample.sample_version == "1.0"
    assert regression.required_verdict == "pass"
    assert regression.registered_at.utcoffset() is not None
    assert regression.schema_version == "1.0.0"


def test_invalid_regression_id_is_rejected() -> None:
    data = valid_regression_data()
    data["regression_id"] = "not-a-uuid"

    with pytest.raises(ValidationError):
        Regression(**data)


def test_invalid_source_finding_id_is_rejected() -> None:
    data = valid_regression_data()
    data["source_finding_id"] = "not-a-uuid"

    with pytest.raises(ValidationError):
        Regression(**data)


def test_invalid_source_retest_id_is_rejected() -> None:
    data = valid_regression_data()
    data["source_retest_id"] = "not-a-uuid"

    with pytest.raises(ValidationError):
        Regression(**data)


def test_invalid_case_id_is_rejected() -> None:
    data = valid_regression_data()
    data["case"] = {
        "case_id": "CASE INVALID!!!",
        "case_version": "1.0",
    }

    with pytest.raises(ValidationError):
        Regression(**data)


def test_blank_case_version_is_rejected() -> None:
    data = valid_regression_data()
    data["case"] = {
        "case_id": "case-direct-pi-001",
        "case_version": "   ",
    }

    with pytest.raises(ValidationError):
        Regression(**data)


def test_invalid_sample_id_is_rejected() -> None:
    data = valid_regression_data()
    data["sample"] = {
        "sample_id": "SAMPLE INVALID!!!",
        "sample_version": "1.0",
    }

    with pytest.raises(ValidationError):
        Regression(**data)


def test_blank_sample_version_is_rejected() -> None:
    data = valid_regression_data()
    data["sample"] = {
        "sample_id": "sample-001",
        "sample_version": "   ",
    }

    with pytest.raises(ValidationError):
        Regression(**data)


def test_non_pass_required_verdict_is_rejected() -> None:
    data = valid_regression_data()
    data["required_verdict"] = "fail"

    with pytest.raises(ValidationError):
        Regression(**data)


def test_naive_registered_at_is_rejected() -> None:
    data = valid_regression_data()
    data["registered_at"] = "2026-09-06T02:00:00"

    with pytest.raises(ValidationError):
        Regression(**data)