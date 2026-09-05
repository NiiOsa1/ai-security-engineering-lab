"""Tests for the Case domain model."""

import pytest
from pydantic import ValidationError

from ai_security_lab.domain.case import Case


def test_case_can_be_created() -> None:
    case = Case(
        case_id="case-direct-pi-001",
        version="1.0",
        security_property=(
            "Untrusted user instructions must not override "
            "protected application instructions."
        ),
        failure_condition=(
            "Protected application instructions are overridden by "
            "untrusted user instructions."
        ),
    )

    assert case.case_id == "case-direct-pi-001"
    assert case.version == "1.0"
    assert case.security_property == (
        "Untrusted user instructions must not override "
        "protected application instructions."
    )
    assert case.failure_condition == (
        "Protected application instructions are overridden by "
        "untrusted user instructions."
    )
    assert case.schema_version == "1.0.0"


def test_invalid_case_id_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Case(
            case_id="CASE 001!!!",
            version="1.0",
            security_property=(
                "Untrusted user instructions must not override "
                "protected application instructions."
            ),
            failure_condition=(
                "Protected application instructions are overridden by "
                "untrusted user instructions."
            ),
        )


def test_blank_case_version_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Case(
            case_id="case-direct-pi-001",
            version="   ",
            security_property=(
                "Untrusted user instructions must not override "
                "protected application instructions."
            ),
            failure_condition=(
                "Protected application instructions are overridden by "
                "untrusted user instructions."
            ),
        )


def test_blank_security_property_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Case(
            case_id="case-direct-pi-001",
            version="1.0",
            security_property="   ",
            failure_condition=(
                "Protected application instructions are overridden by "
                "untrusted user instructions."
            ),
        )


def test_blank_failure_condition_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Case(
            case_id="case-direct-pi-001",
            version="1.0",
            security_property=(
                "Untrusted user instructions must not override "
                "protected application instructions."
            ),
            failure_condition="   ",
        )