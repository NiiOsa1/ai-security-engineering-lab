"""Tests for the Dataset domain model."""

import pytest
from pydantic import ValidationError

from ai_security_lab.domain.dataset import Dataset


def test_dataset_can_be_created() -> None:
    dataset = Dataset(
        dataset_id="prompt-injection-corpus",
        version="3.2",
        provenance_class="research-corpus",
    )

    assert dataset.dataset_id == "prompt-injection-corpus"
    assert dataset.version == "3.2"
    assert dataset.provenance_class == "research-corpus"
    assert dataset.schema_version == "1.0.0"


def test_invalid_dataset_provenance_class_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Dataset(
            dataset_id="invalid-provenance-dataset",
            version="1.0",
            provenance_class="banana",
        )


def test_invalid_dataset_id_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Dataset(
            dataset_id="Prompt Injection Corpus!!!",
            version="1.0",
            provenance_class="synthetic",
        )


def test_blank_dataset_version_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Dataset(
            dataset_id="blank-version-dataset",
            version="   ",
            provenance_class="synthetic",
        )