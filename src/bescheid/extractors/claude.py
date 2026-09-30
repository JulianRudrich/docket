"""Extraction with Claude via the Anthropic API.

Claude reads PDFs and images natively (including scans), so documents are sent
as-is instead of running OCR first.
"""

from __future__ import annotations

import base64
import time
from typing import Any, cast

import anthropic
from anthropic.types import DocumentBlockParam, ImageBlockParam

from bescheid.documents import Document
from bescheid.extractors.base import ExtractionResult
from bescheid.pricing import cost_usd
from bescheid.prompts import load_prompt
from bescheid.schema import LetterExtraction


class ClaudeExtractor:
    def __init__(
        self,
        model: str,
        prompt_version: str = "extraction_v1",
        effort: str | None = None,
        client: anthropic.Anthropic | None = None,
    ) -> None:
        self.model = model
        self.effort = effort
        self.system_prompt = load_prompt(prompt_version)
        self.client = client or anthropic.Anthropic()

    def extract(self, document: Document) -> ExtractionResult:
        start = time.perf_counter()
        extra: dict[str, Any] = {}
        if self.effort:
            extra["output_config"] = {"effort": self.effort}
        try:
            response = self.client.messages.parse(
                model=self.model,
                max_tokens=16000,
                system=self.system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            _document_block(document),
                            {"type": "text", "text": "Extract the information from this letter."},
                        ],
                    }
                ],
                output_format=LetterExtraction,
                **extra,
            )
        except anthropic.APIStatusError as exc:
            # Bad requests and exhausted retries are recorded per document so that
            # one failing letter does not abort an evaluation run.
            return self._failed(document, f"{type(exc).__name__}: {exc.message}", start)
        except anthropic.APIConnectionError as exc:
            return self._failed(document, f"APIConnectionError: {exc}", start)

        usage = response.usage
        error = None
        if response.stop_reason != "end_turn":
            error = f"stop_reason={response.stop_reason}"
        return ExtractionResult(
            doc_id=document.doc_id,
            model=self.model,
            extraction=response.parsed_output if error is None else None,
            error=error,
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            latency_s=time.perf_counter() - start,
            cost_usd=cost_usd(self.model, usage.input_tokens, usage.output_tokens),
        )

    def _failed(self, document: Document, error: str, start: float) -> ExtractionResult:
        return ExtractionResult(
            doc_id=document.doc_id,
            model=self.model,
            extraction=None,
            error=error,
            latency_s=time.perf_counter() - start,
        )


def _document_block(document: Document) -> DocumentBlockParam | ImageBlockParam:
    data = base64.standard_b64encode(document.data).decode("ascii")
    if document.is_pdf:
        return {
            "type": "document",
            "source": {"type": "base64", "media_type": "application/pdf", "data": data},
        }
    source = {"type": "base64", "media_type": document.media_type, "data": data}
    return cast(ImageBlockParam, {"type": "image", "source": source})
