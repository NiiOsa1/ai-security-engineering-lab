"""Tests for the Finding domain model."""

import pytest
from pydantic import ValidationError

from ai_security_lab.domain.finding import Finding


ASSESSMENT_ONE = "550e8400-e29b-41d4-a716-446655440401"
ASSESSMENT_TWO = "550e8400-e29b-41d4-a716-446655440402"


def valid_finding_data() -> dict[str, object]:
    """Return valid Finding input for focused negative tests."""

    return {
        "finding_id": "550e8400-e29b-41d4-a716-446655440500",
        "title": "Unauthorized tool execution through prompt injection",
        "description": (
            "Prompt injection caused the evaluated agent to execute "
            "an action outside the intended authorization boundary."
        ),
        "assessment_ids": [
            ASSESSMENT_ONE,
            ASSESSMENT_TWO,
        ],
        "identified_at": "2026-09-05T22:30:00+00:00",
    }


def test_finding_can_be_created() -> None:
    finding = Finding(**valid_finding_data())

    assert str(finding.finding_id) == (
        "550e8400-e29b-41d4-a716-446655440500"
    )
    assert finding.title == (
        "Unauthorized tool execution through prompt injection"
    )
    assert len(finding.assessment_ids) == 2
    assert finding.identified_at.utcoffset() is not None
    assert finding.schema_version == "1.0.0"


def test_invalid_finding_id_is_rejected() -> None:
    data = valid_finding_data()
    data["finding_id"] = "not-a-uuid"

    with pytest.raises(ValidationError):
        Finding(**data)


def test_blank_title_is_rejected() -> None:
    data = valid_finding_data()
    data["title"] = "   "

    with pytest.raises(ValidationError):
        Finding(**data)


def test_blank_description_is_rejected() -> None:
    data = valid_finding_data()
    data["description"] = "   "

    with pytest.raises(ValidationError):
        Finding(**data)


def test_finding_requires_at_least_one_assessment() -> None:
    data = valid_finding_data()
    data["assessment_ids"] = []

    with pytest.raises(ValidationError):
        Finding(**data)


def test_invalid_assessment_id_is_rejected() -> None:
    data = valid_finding_data()
    data["assessment_ids"] = [
        "not-a-uuid",
    ]

    with pytest.raises(ValidationError):
        Finding(**data)


def test_duplicate_assessment_ids_are_rejected() -> None:
    data = valid_finding_data()
    data["assessment_ids"] = [
        ASSESSMENT_ONE,
        ASSESSMENT_ONE,
    ]

    with pytest.raises(ValidationError):
        Finding(**data)


def test_naive_identified_at_is_rejected() -> None:
    data = valid_finding_data()
    data["identified_at"] = "2026-09-05T22:30:00"

    with pytest.raises(ValidationError):
        Finding(**data)