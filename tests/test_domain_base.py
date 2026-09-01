"""Tests for the shared domain-model foundations."""

import pytest
from pydantic import ValidationError

from ai_security_lab.domain.base import ContractModel, VersionedModel


class ExampleModel(ContractModel):
    """Minimal model used to test shared contract behavior."""

    name: str


def test_versioned_model_has_schema_version() -> None:
    model = VersionedModel()

    assert model.schema_version == "1.0.0"


def test_unexpected_fields_are_rejected() -> None:
    with pytest.raises(ValidationError):
        ExampleModel(name="example", unexpected="value")


def test_assignment_is_revalidated() -> None:
    model = ExampleModel(name="valid")

    with pytest.raises(ValidationError):
        model.name = 123


def test_string_whitespace_is_stripped() -> None:
    model = ExampleModel(name="  example  ")

    assert model.name == "example"