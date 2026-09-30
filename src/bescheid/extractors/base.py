"""Common interface for all extraction backends (API models, local models)."""

from __future__ import annotations

from typing import Protocol

from pydantic import BaseModel

from bescheid.documents import Document
from bescheid.schema import LetterExtraction


class ExtractionResult(BaseModel):
    doc_id: str
    model: str
    extraction: LetterExtraction | None
    error: str | None = None
    input_tokens: int = 0
    output_tokens: int = 0
    latency_s: float = 0.0
    cost_usd: float | None = None


class Extractor(Protocol):
    model: str

    def extract(self, document: Document) -> ExtractionResult: ...
