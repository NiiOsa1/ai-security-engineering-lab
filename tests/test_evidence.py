"""Tests for the Evidence domain model."""

import pytest
from pydantic import ValidationError

from ai_security_lab.domain.evidence import Evidence


VALID_SHA256 = "sha256:" + ("a" * 64)


def valid_evidence_data() -> dict[str, object]:
    """Return valid Evidence input for focused negative tests."""

    return {
        "evidence_id": "550e8400-e29b-41d4-a716-446655440100",
        "run_id": "550e8400-e29b-41d4-a716-446655440000",
        "related_event_ids": [
            "550e8400-e29b-41d4-a716-446655440010",
            "550e8400-e29b-41d4-a716-446655440011",
        ],
        "evidence_kind": "authorization-record",
        "source_component": "policy-engine",
        "collected_at": "2026-09-05T16:00:00+00:00",
        "artifact": {
            "artifact_id": "550e8400-e29b-41d4-a716-446655440200",
            "content_hash": VALID_SHA256,
            "media_type": "application/json",
        },
    }


def test_evidence_can_be_created() -> None:
    evidence = Evidence(**valid_evidence_data())

    assert str(evidence.evidence_id) == (
        "550e8400-e29b-41d4-a716-446655440100"
    )
    assert str(evidence.run_id) == (
        "550e8400-e29b-41d4-a716-446655440000"
    )
    assert len(evidence.related_event_ids) == 2
    assert evidence.evidence_kind == "authorization-record"
    assert evidence.source_component == "policy-engine"
    assert evidence.collected_at.utcoffset() is not None
    assert evidence.sensitivity == "unknown"
    assert evidence.artifact.content_hash == VALID_SHA256
    assert evidence.artifact.media_type == "application/json"
    assert evidence.schema_version == "1.0.0"


def test_invalid_evidence_id_is_rejected() -> None:
    data = valid_evidence_data()
    data["evidence_id"] = "not-a-uuid"

    with pytest.raises(ValidationError):
        Evidence(**data)


def test_invalid_run_id_is_rejected() -> None:
    data = valid_evidence_data()
    data["run_id"] = "not-a-uuid"

    with pytest.raises(ValidationError):
        Evidence(**data)


def test_naive_collected_at_is_rejected() -> None:
    data = valid_evidence_data()
    data["collected_at"] = "2026-09-05T16:00:00"

    with pytest.raises(ValidationError):
        Evidence(**data)


def test_unsupported_evidence_kind_is_rejected() -> None:
    data = valid_evidence_data()
    data["evidence_kind"] = "whatever"

    with pytest.raises(ValidationError):
        Evidence(**data)


def test_blank_source_component_is_rejected() -> None:
    data = valid_evidence_data()
    data["source_component"] = "   "

    with pytest.raises(ValidationError):
        Evidence(**data)


def test_invalid_artifact_digest_is_rejected() -> None:
    data = valid_evidence_data()
    data["artifact"] = {
        "artifact_id": "550e8400-e29b-41d4-a716-446655440200",
        "content_hash": "sha256:abc123",
        "media_type": "application/json",
    }

    with pytest.raises(ValidationError):
        Evidence(**data)


def test_blank_artifact_media_type_is_rejected() -> None:
    data = valid_evidence_data()
    data["artifact"] = {
        "artifact_id": "550e8400-e29b-41d4-a716-446655440200",
        "content_hash": VALID_SHA256,
        "media_type": "   ",
    }

    with pytest.raises(ValidationError):
        Evidence(**data)


def test_duplicate_related_event_ids_are_rejected() -> None:
    data = valid_evidence_data()
    data["related_event_ids"] = [
        "550e8400-e29b-41d4-a716-446655440010",
        "550e8400-e29b-41d4-a716-446655440010",
    ]

    with pytest.raises(ValidationError):
        Evidence(**data)


def test_unsupported_sensitivity_is_rejected() -> None:
    data = valid_evidence_data()
    data["sensitivity"] = "public"

    with pytest.raises(ValidationError):
        Evidence(**data)