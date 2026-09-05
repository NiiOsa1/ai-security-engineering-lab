"""Tests for the Campaign domain model."""

import pytest
from pydantic import ValidationError

from ai_security_lab.domain.campaign import Campaign


def test_campaign_can_be_created() -> None:
    campaign = Campaign(
        campaign_id="campaign-prompt-injection-001",
        version="1.0",
        target={
            "target_id": "agent-001",
            "target_version": "2.1",
        },
        environment={
            "environment_id": "env-hardened-001",
            "environment_version": "1.0",
        },
        cases=[
            {
                "case_id": "case-direct-pi-001",
                "case_version": "1.0",
            },
            {
                "case_id": "case-indirect-pi-001",
                "case_version": "1.0",
            },
        ],
        repetitions_per_case=5,
    )

    assert campaign.campaign_id == "campaign-prompt-injection-001"
    assert campaign.version == "1.0"
    assert campaign.target.target_id == "agent-001"
    assert campaign.target.target_version == "2.1"
    assert campaign.environment.environment_id == "env-hardened-001"
    assert campaign.environment.environment_version == "1.0"
    assert len(campaign.cases) == 2
    assert campaign.cases[0].case_id == "case-direct-pi-001"
    assert campaign.cases[1].case_id == "case-indirect-pi-001"
    assert campaign.repetitions_per_case == 5
    assert campaign.schema_version == "1.0.0"


def test_invalid_campaign_id_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Campaign(
            campaign_id="CAMPAIGN 001!!!",
            version="1.0",
            target={
                "target_id": "agent-001",
                "target_version": "2.1",
            },
            environment={
                "environment_id": "env-hardened-001",
                "environment_version": "1.0",
            },
            cases=[
                {
                    "case_id": "case-direct-pi-001",
                    "case_version": "1.0",
                }
            ],
        )


def test_blank_campaign_version_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Campaign(
            campaign_id="campaign-prompt-injection-001",
            version="   ",
            target={
                "target_id": "agent-001",
                "target_version": "2.1",
            },
            environment={
                "environment_id": "env-hardened-001",
                "environment_version": "1.0",
            },
            cases=[
                {
                    "case_id": "case-direct-pi-001",
                    "case_version": "1.0",
                }
            ],
        )


def test_campaign_requires_at_least_one_case() -> None:
    with pytest.raises(ValidationError):
        Campaign(
            campaign_id="campaign-prompt-injection-001",
            version="1.0",
            target={
                "target_id": "agent-001",
                "target_version": "2.1",
            },
            environment={
                "environment_id": "env-hardened-001",
                "environment_version": "1.0",
            },
            cases=[],
        )


def test_repetitions_per_case_must_be_positive() -> None:
    with pytest.raises(ValidationError):
        Campaign(
            campaign_id="campaign-prompt-injection-001",
            version="1.0",
            target={
                "target_id": "agent-001",
                "target_version": "2.1",
            },
            environment={
                "environment_id": "env-hardened-001",
                "environment_version": "1.0",
            },
            cases=[
                {
                    "case_id": "case-direct-pi-001",
                    "case_version": "1.0",
                }
            ],
            repetitions_per_case=0,
        )


def test_duplicate_case_id_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Campaign(
            campaign_id="campaign-prompt-injection-001",
            version="1.0",
            target={
                "target_id": "agent-001",
                "target_version": "2.1",
            },
            environment={
                "environment_id": "env-hardened-001",
                "environment_version": "1.0",
            },
            cases=[
                {
                    "case_id": "case-direct-pi-001",
                    "case_version": "1.0",
                },
                {
                    "case_id": "case-direct-pi-001",
                    "case_version": "2.0",
                },
            ],
        )