"""Tests for the Run domain model."""

import pytest
from pydantic import ValidationError

from ai_security_lab.domain.run import Run


def test_run_can_be_created() -> None:
    run = Run(
        run_id="550e8400-e29b-41d4-a716-446655440000",
        campaign={
            "campaign_id": "campaign-prompt-injection-001",
            "campaign_version": "1.0",
        },
        target={
            "target_id": "agent-001",
            "target_version": "2.1",
        },
        environment={
            "environment_id": "env-hardened-001",
            "environment_version": "1.0",
        },
        case={
            "case_id": "case-direct-pi-001",
            "case_version": "1.0",
        },
        sample={
            "sample_id": "sample-001",
            "sample_version": "1.0",
        },
        started_at="2026-09-05T14:30:00+00:00",
        execution_provenance={
            "kind": "git-commit",
            "value": (
                "0123456789abcdef"
                "0123456789abcdef"
                "01234567"
            ),
        },
    )

    assert str(run.run_id) == "550e8400-e29b-41d4-a716-446655440000"
    assert run.campaign.campaign_id == "campaign-prompt-injection-001"
    assert run.target.target_id == "agent-001"
    assert run.environment.environment_id == "env-hardened-001"
    assert run.case.case_id == "case-direct-pi-001"
    assert run.sample.sample_id == "sample-001"
    assert run.started_at.utcoffset() is not None
    assert run.execution_provenance.kind == "git-commit"
    assert run.schema_version == "1.0.0"


def test_invalid_run_id_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Run(
            run_id="not-a-uuid",
            campaign={
                "campaign_id": "campaign-prompt-injection-001",
                "campaign_version": "1.0",
            },
            target={
                "target_id": "agent-001",
                "target_version": "2.1",
            },
            environment={
                "environment_id": "env-hardened-001",
                "environment_version": "1.0",
            },
            case={
                "case_id": "case-direct-pi-001",
                "case_version": "1.0",
            },
            sample={
                "sample_id": "sample-001",
                "sample_version": "1.0",
            },
            started_at="2026-09-05T14:30:00+00:00",
            execution_provenance={
                "kind": "package-version",
                "value": "0.1.0",
            },
        )


def test_naive_started_at_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Run(
            run_id="550e8400-e29b-41d4-a716-446655440000",
            campaign={
                "campaign_id": "campaign-prompt-injection-001",
                "campaign_version": "1.0",
            },
            target={
                "target_id": "agent-001",
                "target_version": "2.1",
            },
            environment={
                "environment_id": "env-hardened-001",
                "environment_version": "1.0",
            },
            case={
                "case_id": "case-direct-pi-001",
                "case_version": "1.0",
            },
            sample={
                "sample_id": "sample-001",
                "sample_version": "1.0",
            },
            started_at="2026-09-05T14:30:00",
            execution_provenance={
                "kind": "package-version",
                "value": "0.1.0",
            },
        )


def test_blank_execution_provenance_value_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Run(
            run_id="550e8400-e29b-41d4-a716-446655440000",
            campaign={
                "campaign_id": "campaign-prompt-injection-001",
                "campaign_version": "1.0",
            },
            target={
                "target_id": "agent-001",
                "target_version": "2.1",
            },
            environment={
                "environment_id": "env-hardened-001",
                "environment_version": "1.0",
            },
            case={
                "case_id": "case-direct-pi-001",
                "case_version": "1.0",
            },
            sample={
                "sample_id": "sample-001",
                "sample_version": "1.0",
            },
            started_at="2026-09-05T14:30:00+00:00",
            execution_provenance={
                "kind": "package-version",
                "value": "   ",
            },
        )


def test_unsupported_execution_provenance_kind_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Run(
            run_id="550e8400-e29b-41d4-a716-446655440000",
            campaign={
                "campaign_id": "campaign-prompt-injection-001",
                "campaign_version": "1.0",
            },
            target={
                "target_id": "agent-001",
                "target_version": "2.1",
            },
            environment={
                "environment_id": "env-hardened-001",
                "environment_version": "1.0",
            },
            case={
                "case_id": "case-direct-pi-001",
                "case_version": "1.0",
            },
            sample={
                "sample_id": "sample-001",
                "sample_version": "1.0",
            },
            started_at="2026-09-05T14:30:00+00:00",
            execution_provenance={
                "kind": "github",
                "value": "anything",
            },
        )


def test_invalid_git_commit_provenance_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Run(
            run_id="550e8400-e29b-41d4-a716-446655440000",
            campaign={
                "campaign_id": "campaign-prompt-injection-001",
                "campaign_version": "1.0",
            },
            target={
                "target_id": "agent-001",
                "target_version": "2.1",
            },
            environment={
                "environment_id": "env-hardened-001",
                "environment_version": "1.0",
            },
            case={
                "case_id": "case-direct-pi-001",
                "case_version": "1.0",
            },
            sample={
                "sample_id": "sample-001",
                "sample_version": "1.0",
            },
            started_at="2026-09-05T14:30:00+00:00",
            execution_provenance={
                "kind": "git-commit",
                "value": "abc123",
            },
        )


def test_invalid_oci_digest_provenance_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Run(
            run_id="550e8400-e29b-41d4-a716-446655440000",
            campaign={
                "campaign_id": "campaign-prompt-injection-001",
                "campaign_version": "1.0",
            },
            target={
                "target_id": "agent-001",
                "target_version": "2.1",
            },
            environment={
                "environment_id": "env-hardened-001",
                "environment_version": "1.0",
            },
            case={
                "case_id": "case-direct-pi-001",
                "case_version": "1.0",
            },
            sample={
                "sample_id": "sample-001",
                "sample_version": "1.0",
            },
            started_at="2026-09-05T14:30:00+00:00",
            execution_provenance={
                "kind": "oci-digest",
                "value": "sha256:abc123",
            },
        )