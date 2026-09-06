"""Tests for the Remediation domain model."""

import pytest
from pydantic import ValidationError

from ai_security_lab.domain.remediation import Remediation


FINDING_ONE = "550e8400-e29b-41d4-a716-446655440501"
FINDING_TWO = "550e8400-e29b-41d4-a716-446655440502"


def valid_remediation_data() -> dict[str, object]:
    """Return valid Remediation input for focused negative tests."""

    return {
        "remediation_id": "550e8400-e29b-41d4-a716-446655440600",
        "finding_ids": [
            FINDING_ONE,
            FINDING_TWO,
        ],
        "intended_change": (
            "Enforce deterministic authorization before tool execution "
            "and deny actions outside the task-scoped permission set."
        ),
        "proposed_at": "2026-09-06T01:15:00+00:00",
    }


def test_remediation_can_be_created() -> None:
    remediation = Remediation(**valid_remediation_data())

    assert str(remediation.remediation_id) == (
        "550e8400-e29b-41d4-a716-446655440600"
    )
    assert len(remediation.finding_ids) == 2
    assert remediation.intended_change.startswith(
        "Enforce deterministic authorization"
    )
    assert remediation.proposed_at.utcoffset() is not None
    assert remediation.schema_version == "1.0.0"


def test_invalid_remediation_id_is_rejected() -> None:
    data = valid_remediation_data()
    data["remediation_id"] = "not-a-uuid"

    with pytest.raises(ValidationError):
        Remediation(**data)


def test_remediation_requires_at_least_one_finding() -> None:
    data = valid_remediation_data()
    data["finding_ids"] = []

    with pytest.raises(ValidationError):
        Remediation(**data)


def test_invalid_finding_id_is_rejected() -> None:
    data = valid_remediation_data()
    data["finding_ids"] = [
        "not-a-uuid",
    ]

    with pytest.raises(ValidationError):
        Remediation(**data)


def test_duplicate_finding_ids_are_rejected() -> None:
    data = valid_remediation_data()
    data["finding_ids"] = [
        FINDING_ONE,
        FINDING_ONE,
    ]

    with pytest.raises(ValidationError):
        Remediation(**data)


def test_blank_intended_change_is_rejected() -> None:
    data = valid_remediation_data()
    data["intended_change"] = "   "

    with pytest.raises(ValidationError):
        Remediation(**data)


def test_naive_proposed_at_is_rejected() -> None:
    data = valid_remediation_data()
    data["proposed_at"] = "2026-09-06T01:15:00"

    with pytest.raises(ValidationError):
        Remediation(**data)