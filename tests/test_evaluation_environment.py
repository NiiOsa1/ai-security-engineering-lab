"""Tests for the Evaluation Environment domain model."""

import pytest
from pydantic import ValidationError

from ai_security_lab.domain.evaluation_environment import EvaluationEnvironment


def test_evaluation_environment_can_be_created() -> None:
    environment = EvaluationEnvironment(
        environment_id="env-permissive-001",
        version="1.0",
    )

    assert environment.environment_id == "env-permissive-001"
    assert environment.version == "1.0"
    assert environment.schema_version == "1.0.0"


def test_invalid_environment_id_is_rejected() -> None:
    with pytest.raises(ValidationError):
        EvaluationEnvironment(
            environment_id="ENV 001!!!",
            version="1.0",
        )


def test_blank_environment_version_is_rejected() -> None:
    with pytest.raises(ValidationError):
        EvaluationEnvironment(
            environment_id="env-permissive-001",
            version="   ",
        )


def test_environment_can_record_control_state() -> None:
    environment = EvaluationEnvironment(
        environment_id="env-hardened-001",
        version="1.0",
        controls=[
            {
                "control_id": "authz-003",
                "control_version": "2.1",
                "state": "enabled",
            }
        ],
    )

    assert environment.controls[0].control_id == "authz-003"
    assert environment.controls[0].control_version == "2.1"
    assert environment.controls[0].state == "enabled"


def test_invalid_control_state_is_rejected() -> None:
    with pytest.raises(ValidationError):
        EvaluationEnvironment(
            environment_id="env-hardened-001",
            version="1.0",
            controls=[
                {
                    "control_id": "authz-003",
                    "control_version": "2.1",
                    "state": "active",
                }
            ],
        )


def test_environment_can_record_multiple_controls() -> None:
    environment = EvaluationEnvironment(
        environment_id="env-hardened-001",
        version="1.0",
        controls=[
            {
                "control_id": "authz-003",
                "control_version": "2.1",
                "state": "enabled",
            },
            {
                "control_id": "egress-002",
                "control_version": "1.0",
                "state": "enabled",
            },
            {
                "control_id": "detector-004",
                "control_version": "3.0",
                "state": "observe-only",
            },
        ],
    )

    assert len(environment.controls) == 3
    assert environment.controls[0].control_id == "authz-003"
    assert environment.controls[1].control_id == "egress-002"
    assert environment.controls[2].state == "observe-only"


def test_duplicate_control_id_is_rejected() -> None:
    with pytest.raises(ValidationError):
        EvaluationEnvironment(
            environment_id="env-hardened-001",
            version="1.0",
            controls=[
                {
                    "control_id": "authz-003",
                    "control_version": "2.1",
                    "state": "enabled",
                },
                {
                    "control_id": "authz-003",
                    "control_version": "2.1",
                    "state": "disabled",
                },
            ],
        )