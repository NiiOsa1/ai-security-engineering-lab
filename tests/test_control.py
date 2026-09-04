"""Tests for the Control domain model."""

import pytest
from pydantic import ValidationError

from ai_security_lab.domain.control import Control


def test_control_can_be_created() -> None:
    control = Control(
        control_id="authz-003",
        name="External authorization policy",
        version="2.1",
        control_classes=["restrictive", "containment"],
    )

    assert control.control_id == "authz-003"
    assert control.name == "External authorization policy"
    assert control.version == "2.1"
    assert control.control_classes == ["restrictive", "containment"]
    assert control.schema_version == "1.0.0"


def test_invalid_control_id_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Control(
            control_id="AUTHZ 003!!!",
            name="External authorization policy",
            version="2.1",
        )


def test_blank_control_version_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Control(
            control_id="authz-003",
            name="External authorization policy",
            version="   ",
        )


def test_blank_control_name_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Control(
            control_id="authz-003",
            name="   ",
            version="2.1",
        )


def test_invalid_control_class_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Control(
            control_id="authz-003",
            name="External authorization policy",
            version="2.1",
            control_classes=["banana"],
        )