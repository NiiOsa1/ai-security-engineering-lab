"""Tests for the Trajectory domain model."""

import pytest
from pydantic import ValidationError

from ai_security_lab.domain.trajectory import Trajectory


def test_trajectory_can_be_created() -> None:
    trajectory = Trajectory(
        trajectory_id="550e8400-e29b-41d4-a716-446655440001",
        run_id="550e8400-e29b-41d4-a716-446655440000",
        events=[
            {
                "event_id": "550e8400-e29b-41d4-a716-446655440010",
                "recorded_sequence": 1,
                "event_type": "input-received",
                "occurred_at": "2026-09-05T15:00:00+00:00",
            },
            {
                "event_id": "550e8400-e29b-41d4-a716-446655440011",
                "recorded_sequence": 2,
                "event_type": "model-invocation",
                "occurred_at": "2026-09-05T15:00:01+00:00",
            },
            {
                "event_id": "550e8400-e29b-41d4-a716-446655440012",
                "recorded_sequence": 3,
                "event_type": "action-proposed",
                "occurred_at": "2026-09-05T15:00:02+00:00",
            },
        ],
    )

    assert str(trajectory.trajectory_id) == (
        "550e8400-e29b-41d4-a716-446655440001"
    )
    assert str(trajectory.run_id) == (
        "550e8400-e29b-41d4-a716-446655440000"
    )
    assert len(trajectory.events) == 3
    assert trajectory.events[0].recorded_sequence == 1
    assert trajectory.events[1].event_type == "model-invocation"
    assert trajectory.events[2].event_type == "action-proposed"
    assert trajectory.events[0].occurred_at.utcoffset() is not None
    assert trajectory.schema_version == "1.0.0"


def test_invalid_trajectory_id_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Trajectory(
            trajectory_id="not-a-uuid",
            run_id="550e8400-e29b-41d4-a716-446655440000",
            events=[],
        )


def test_invalid_run_id_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Trajectory(
            trajectory_id="550e8400-e29b-41d4-a716-446655440001",
            run_id="not-a-uuid",
            events=[],
        )


def test_naive_event_timestamp_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Trajectory(
            trajectory_id="550e8400-e29b-41d4-a716-446655440001",
            run_id="550e8400-e29b-41d4-a716-446655440000",
            events=[
                {
                    "event_id": "550e8400-e29b-41d4-a716-446655440010",
                    "recorded_sequence": 1,
                    "event_type": "input-received",
                    "occurred_at": "2026-09-05T15:00:00",
                }
            ],
        )


def test_unsupported_event_type_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Trajectory(
            trajectory_id="550e8400-e29b-41d4-a716-446655440001",
            run_id="550e8400-e29b-41d4-a716-446655440000",
            events=[
                {
                    "event_id": "550e8400-e29b-41d4-a716-446655440010",
                    "recorded_sequence": 1,
                    "event_type": "openai-tool-call",
                    "occurred_at": "2026-09-05T15:00:00+00:00",
                }
            ],
        )


def test_duplicate_event_id_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Trajectory(
            trajectory_id="550e8400-e29b-41d4-a716-446655440001",
            run_id="550e8400-e29b-41d4-a716-446655440000",
            events=[
                {
                    "event_id": "550e8400-e29b-41d4-a716-446655440010",
                    "recorded_sequence": 1,
                    "event_type": "model-invocation",
                    "occurred_at": "2026-09-05T15:00:00+00:00",
                },
                {
                    "event_id": "550e8400-e29b-41d4-a716-446655440010",
                    "recorded_sequence": 2,
                    "event_type": "model-output",
                    "occurred_at": "2026-09-05T15:00:01+00:00",
                },
            ],
        )


def test_gapped_recorded_sequence_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Trajectory(
            trajectory_id="550e8400-e29b-41d4-a716-446655440001",
            run_id="550e8400-e29b-41d4-a716-446655440000",
            events=[
                {
                    "event_id": "550e8400-e29b-41d4-a716-446655440010",
                    "recorded_sequence": 1,
                    "event_type": "model-invocation",
                    "occurred_at": "2026-09-05T15:00:00+00:00",
                },
                {
                    "event_id": "550e8400-e29b-41d4-a716-446655440011",
                    "recorded_sequence": 3,
                    "event_type": "model-output",
                    "occurred_at": "2026-09-05T15:00:01+00:00",
                },
            ],
        )


def test_out_of_order_recorded_sequence_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Trajectory(
            trajectory_id="550e8400-e29b-41d4-a716-446655440001",
            run_id="550e8400-e29b-41d4-a716-446655440000",
            events=[
                {
                    "event_id": "550e8400-e29b-41d4-a716-446655440010",
                    "recorded_sequence": 2,
                    "event_type": "model-output",
                    "occurred_at": "2026-09-05T15:00:01+00:00",
                },
                {
                    "event_id": "550e8400-e29b-41d4-a716-446655440011",
                    "recorded_sequence": 1,
                    "event_type": "model-invocation",
                    "occurred_at": "2026-09-05T15:00:00+00:00",
                },
            ],
        )


def test_empty_trajectory_is_allowed_when_explicit() -> None:
    trajectory = Trajectory(
        trajectory_id="550e8400-e29b-41d4-a716-446655440001",
        run_id="550e8400-e29b-41d4-a716-446655440000",
        events=[],
    )

    assert trajectory.events == []