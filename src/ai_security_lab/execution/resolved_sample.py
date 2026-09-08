"""Execution-ready Evaluation Sample contract."""

from hashlib import sha256
from typing import Self

from pydantic import ConfigDict, Field, model_validator

from ai_security_lab.domain.base import ContractModel
from ai_security_lab.domain.evaluation_sample import (
    ContentHash,
    MediaType,
    SampleId,
    SampleVersion,
)


class ResolvedEvaluationSample(ContractModel):
    """An immutable, integrity-verified snapshot of evaluation sample bytes."""

    model_config = ConfigDict(
        frozen=True,
    )

    sample_id: SampleId
    sample_version: SampleVersion
    content_hash: ContentHash
    media_type: MediaType
    content: bytes = Field(
        strict=True,
        repr=False,
        exclude=True,
    )

    @model_validator(mode="after")
    def validate_content_integrity(self) -> Self:
        actual_hash = f"sha256:{sha256(self.content).hexdigest()}"

        if actual_hash != self.content_hash:
            raise ValueError(
                "resolved sample content does not match declared content_hash"
            )

        return self