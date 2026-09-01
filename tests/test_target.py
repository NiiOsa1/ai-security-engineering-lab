"""Tests for the Target domain model."""

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