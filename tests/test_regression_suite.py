"""Tests for the Regression Suite domain model."""

import pytest
from pydantic import ValidationError

from ai_security_lab.domain.regression_suite import RegressionSuite


REGRESSION_ONE = "550e8400-e29b-41d4-a716-446655440801"
REGRESSION_TWO = "550e8400-e29b-41d4-a716-446655440802"


def valid_regression_suite_data() -> dict[str, object]:
    """Return valid Regression Suite input for focused negative tests."""

    return {
        "suite_id": "prompt-injection-core",
        "version": "1.0",
        "regression_ids": [
            REGRESSION_ONE,
            REGRESSION_TWO,
        ],
    }


def test_regression_suite_can_be_created() -> None:
    suite = RegressionSuite(**valid_regression_suite_data())

    assert suite.suite_id == "prompt-injection-core"
    assert suite.version == "1.0"
    assert len(suite.regression_ids) == 2
    assert str(suite.regression_ids[0]) == REGRESSION_ONE
    assert str(suite.regression_ids[1]) == REGRESSION_TWO
    assert suite.schema_version == "1.0.0"


def test_invalid_suite_id_is_rejected() -> None:
    data = valid_regression_suite_data()
    data["suite_id"] = "Prompt Injection!!!"

    with pytest.raises(ValidationError):
        RegressionSuite(**data)


def test_blank_suite_version_is_rejected() -> None:
    data = valid_regression_suite_data()
    data["version"] = "   "

    with pytest.raises(ValidationError):
        RegressionSuite(**data)


def test_regression_suite_requires_at_least_one_regression() -> None:
    data = valid_regression_suite_data()
    data["regression_ids"] = []

    with pytest.raises(ValidationError):
        RegressionSuite(**data)


def test_invalid_regression_id_is_rejected() -> None:
    data = valid_regression_suite_data()
    data["regression_ids"] = [
        "not-a-uuid",
    ]

    with pytest.raises(ValidationError):
        RegressionSuite(**data)


def test_duplicate_regression_ids_are_rejected() -> None:
    data = valid_regression_suite_data()
    data["regression_ids"] = [
        REGRESSION_ONE,
        REGRESSION_ONE,
    ]

    with pytest.raises(ValidationError):
        RegressionSuite(**data)