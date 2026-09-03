"""Tests for the Target domain model."""

import pytest
from pydantic import ValidationError

from ai_security_lab.domain.target import Target


def test_target_can_be_created() -> None:
    target = Target(
        target_id="voice-agent-001",
        name="Reference Voice Agent",
        target_type="voice",
    )

    assert target.target_id == "voice-agent-001"
    assert target.name == "Reference Voice Agent"
    assert target.target_type == "voice"
    assert target.schema_version == "1.0.0"


def test_invalid_target_type_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Target(
            target_id="invalid-target-001",
            name="Invalid Target",
            target_type="banana",
        )


def test_invalid_target_id_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Target(
            target_id="Voice Agent!!!",
            name="Invalid Identifier Target",
            target_type="voice",
        )


def test_blank_target_name_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Target(
            target_id="blank-name-target-001",
            name="   ",
            target_type="voice",
        )