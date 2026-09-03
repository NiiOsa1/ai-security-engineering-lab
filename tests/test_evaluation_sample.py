"""Tests for the Evaluation Sample domain model."""

import pytest
from pydantic import ValidationError

from ai_security_lab.domain.evaluation_sample import EvaluationSample


VALID_CONTENT_HASH = (
    "sha256:"
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
)


def test_evaluation_sample_can_be_created() -> None:
    sample = EvaluationSample(
        sample_id="sample-004817",
        version="1.0",
        content_hash=VALID_CONTENT_HASH,
    )

    assert sample.sample_id == "sample-004817"
    assert sample.version == "1.0"
    assert sample.content_hash == VALID_CONTENT_HASH
    assert sample.schema_version == "1.0.0"


def test_invalid_content_hash_is_rejected() -> None:
    with pytest.raises(ValidationError):
        EvaluationSample(
            sample_id="sample-invalid-hash",
            version="1.0",
            content_hash="sha256:not-a-real-digest",
        )


def test_invalid_sample_id_is_rejected() -> None:
    with pytest.raises(ValidationError):
        EvaluationSample(
            sample_id="Sample 004817!!!",
            version="1.0",
            content_hash=VALID_CONTENT_HASH,
        )


def test_blank_sample_version_is_rejected() -> None:
    with pytest.raises(ValidationError):
        EvaluationSample(
            sample_id="sample-blank-version",
            version="   ",
            content_hash=VALID_CONTENT_HASH,
        )