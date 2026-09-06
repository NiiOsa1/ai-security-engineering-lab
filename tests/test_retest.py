"""Tests for the Retest domain model."""

import pytest
from pydantic import ValidationError

from ai_security_lab.domain.retest import Retest


def valid_retest_data() -> dict[str, object]:
    """Return valid Retest input for focused negative tests."""

    return {
        "retest_id": "550e8400-e29b-41d4-a716-446655440700",
        "finding_id": "550e8400-e29b-41d4-a716-446655440500",
        "remediation_id": "550e8400-e29b-41d4-a716-446655440600",
        "run_id": "550e8400-e29b-41d4-a716-446655440701",
        "assessment_id": "550e8400-e29b-41d4-a716-446655440702",
    }


def test_retest_can_be_created() -> None:
    retest = Retest(**valid_retest_data())

    assert str(retest.retest_id) == (
        "550e8400-e29b-41d4-a716-446655440700"
    )
    assert str(retest.finding_id) == (
        "550e8400-e29b-41d4-a716-446655440500"
    )
    assert str(retest.remediation_id) == (
        "550e8400-e29b-41d4-a716-446655440600"
    )
    assert str(retest.run_id) == (
        "550e8400-e29b-41d4-a716-446655440701"
    )
    assert str(retest.assessment_id) == (
        "550e8400-e29b-41d4-a716-446655440702"
    )
    assert retest.schema_version == "1.0.0"


def test_invalid_retest_id_is_rejected() -> None:
    data = valid_retest_data()
    data["retest_id"] = "not-a-uuid"

    with pytest.raises(ValidationError):
        Retest(**data)


def test_invalid_finding_id_is_rejected() -> None:
    data = valid_retest_data()
    data["finding_id"] = "not-a-uuid"

    with pytest.raises(ValidationError):
        Retest(**data)


def test_invalid_remediation_id_is_rejected() -> None:
    data = valid_retest_data()
    data["remediation_id"] = "not-a-uuid"

    with pytest.raises(ValidationError):
        Retest(**data)


def test_invalid_run_id_is_rejected() -> None:
    data = valid_retest_data()
    data["run_id"] = "not-a-uuid"

    with pytest.raises(ValidationError):
        Retest(**data)


def test_invalid_assessment_id_is_rejected() -> None:
    data = valid_retest_data()
    data["assessment_id"] = "not-a-uuid"

    with pytest.raises(ValidationError):
        Retest(**data)