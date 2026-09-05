"""Tests for the Outcome domain model."""

import pytest
from pydantic import ValidationError

from ai_security_lab.domain.outcome import Outcome


EVIDENCE_ACTION = "550e8400-e29b-41d4-a716-446655440101"
EVIDENCE_AUTHORIZATION = "550e8400-e29b-41d4-a716-446655440102"
EVIDENCE_EXECUTION = "550e8400-e29b-41d4-a716-446655440103"
EVIDENCE_EXTERNAL_STATE = "550e8400-e29b-41d4-a716-446655440104"


def valid_outcome_data() -> dict[str, object]:
    """Return valid Outcome input for focused tests."""

    return {
        "outcome_id": "550e8400-e29b-41d4-a716-446655440300",
        "run_id": "550e8400-e29b-41d4-a716-446655440000",
        "action_proposed": {
            "state": "yes",
            "evidence_ids": [EVIDENCE_ACTION],
        },
        "authorization_granted": {
            "state": "no",
            "evidence_ids": [EVIDENCE_AUTHORIZATION],
        },
        "execution_attempted": {
            "state": "no",
            "evidence_ids": [EVIDENCE_AUTHORIZATION],
        },
        "execution_occurred": {
            "state": "no",
            "evidence_ids": [EVIDENCE_EXECUTION],
        },
        "external_effect_occurred": {
            "state": "no",
            "evidence_ids": [EVIDENCE_EXTERNAL_STATE],
        },
        "detection_occurred": {
            "state": "unknown",
            "evidence_ids": [],
        },
        "containment_occurred": {
            "state": "yes",
            "evidence_ids": [EVIDENCE_AUTHORIZATION],
        },
        "recovery_occurred": {
            "state": "not-applicable",
            "evidence_ids": [],
        },
    }


def test_outcome_can_be_created() -> None:
    outcome = Outcome(**valid_outcome_data())

    assert str(outcome.outcome_id) == (
        "550e8400-e29b-41d4-a716-446655440300"
    )
    assert str(outcome.run_id) == (
        "550e8400-e29b-41d4-a716-446655440000"
    )
    assert outcome.action_proposed.state == "yes"
    assert outcome.authorization_granted.state == "no"
    assert outcome.execution_occurred.state == "no"
    assert outcome.external_effect_occurred.state == "no"
    assert outcome.detection_occurred.state == "unknown"
    assert outcome.recovery_occurred.state == "not-applicable"
    assert outcome.schema_version == "1.0.0"


def test_invalid_outcome_id_is_rejected() -> None:
    data = valid_outcome_data()
    data["outcome_id"] = "not-a-uuid"

    with pytest.raises(ValidationError):
        Outcome(**data)


def test_invalid_run_id_is_rejected() -> None:
    data = valid_outcome_data()
    data["run_id"] = "not-a-uuid"

    with pytest.raises(ValidationError):
        Outcome(**data)


def test_yes_state_without_evidence_is_rejected() -> None:
    data = valid_outcome_data()
    data["action_proposed"] = {
        "state": "yes",
        "evidence_ids": [],
    }

    with pytest.raises(ValidationError):
        Outcome(**data)


def test_no_state_without_evidence_is_rejected() -> None:
    data = valid_outcome_data()
    data["execution_occurred"] = {
        "state": "no",
        "evidence_ids": [],
    }

    with pytest.raises(ValidationError):
        Outcome(**data)


def test_unknown_state_without_evidence_is_allowed() -> None:
    data = valid_outcome_data()
    data["detection_occurred"] = {
        "state": "unknown",
        "evidence_ids": [],
    }

    outcome = Outcome(**data)

    assert outcome.detection_occurred.state == "unknown"
    assert outcome.detection_occurred.evidence_ids == []


def test_not_applicable_state_without_evidence_is_allowed() -> None:
    data = valid_outcome_data()
    data["recovery_occurred"] = {
        "state": "not-applicable",
        "evidence_ids": [],
    }

    outcome = Outcome(**data)

    assert outcome.recovery_occurred.state == "not-applicable"


def test_duplicate_evidence_ids_are_rejected() -> None:
    data = valid_outcome_data()
    data["action_proposed"] = {
        "state": "yes",
        "evidence_ids": [
            EVIDENCE_ACTION,
            EVIDENCE_ACTION,
        ],
    }

    with pytest.raises(ValidationError):
        Outcome(**data)


def test_unsupported_fact_state_is_rejected() -> None:
    data = valid_outcome_data()
    data["authorization_granted"] = {
        "state": "probably",
        "evidence_ids": [EVIDENCE_AUTHORIZATION],
    }

    with pytest.raises(ValidationError):
        Outcome(**data)


def test_fact_state_is_required() -> None:
    data = valid_outcome_data()
    data["external_effect_occurred"] = {
        "evidence_ids": [EVIDENCE_EXTERNAL_STATE],
    }

    with pytest.raises(ValidationError):
        Outcome(**data)