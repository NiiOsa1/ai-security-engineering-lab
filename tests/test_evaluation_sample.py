"""Tests for the Evaluation Sample domain model."""

import pytest
from pydantic import ValidationError

from ai_security_lab.domain.evaluation_sample import EvaluationSample


VALID_CONTENT_HASH = (
    "sha256:"
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
)


def valid_evaluation_sample_data() -> dict[str, object]:
    return {
        "sample_id": "sample-004817",
        "version": "1.0",
        "content_hash": VALID_CONTENT_HASH,
        "media_type": "text/plain",
    }


def test_evaluation_sample_can_be_created() -> None:
    sample = EvaluationSample(**valid_evaluation_sample_data())

    assert sample.sample_id == "sample-004817"
    assert sample.version == "1.0"
    assert sample.content_hash == VALID_CONTENT_HASH
    assert sample.media_type == "text/plain"
    assert sample.schema_version == "1.0.0"


def test_invalid_content_hash_is_rejected() -> None:
    data = valid_evaluation_sample_data()
    data["content_hash"] = "sha256:not-a-real-digest"

    with pytest.raises(ValidationError):
        EvaluationSample(**data)


def test_invalid_sample_id_is_rejected() -> None:
    data = valid_evaluation_sample_data()
    data["sample_id"] = "Sample 004817!!!"

    with pytest.raises(ValidationError):
        EvaluationSample(**data)


def test_blank_sample_version_is_rejected() -> None:
    data = valid_evaluation_sample_data()
    data["version"] = "   "

    with pytest.raises(ValidationError):
        EvaluationSample(**data)


def test_missing_media_type_is_rejected() -> None:
    data = valid_evaluation_sample_data()
    del data["media_type"]

    with pytest.raises(ValidationError):
        EvaluationSample(**data)


def test_blank_media_type_is_rejected() -> None:
    data = valid_evaluation_sample_data()
    data["media_type"] = "   "

    with pytest.raises(ValidationError):
        EvaluationSample(**data)


def test_media_type_below_minimum_length_is_rejected() -> None:
    data = valid_evaluation_sample_data()
    data["media_type"] = "ab"

    with pytest.raises(ValidationError):
        EvaluationSample(**data)


def test_media_type_above_maximum_length_is_rejected() -> None:
    data = valid_evaluation_sample_data()
    data["media_type"] = "a" * 256

    with pytest.raises(ValidationError):
        EvaluationSample(**data)


def test_non_string_media_type_is_rejected() -> None:
    data = valid_evaluation_sample_data()
    data["media_type"] = b"text/plain"

    with pytest.raises(ValidationError):
        EvaluationSample(**data)