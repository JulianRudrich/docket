"""Tests for the Claude backend with a fake client (no network, no cost)."""

from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from bescheid.documents import load_document
from bescheid.extractors.claude import ClaudeExtractor
from bescheid.schema import LetterExtraction


class FakeMessages:
    def __init__(self, response: Any) -> None:
        self.response = response
        self.calls: list[dict[str, Any]] = []

    def parse(self, **kwargs: Any) -> Any:
        self.calls.append(kwargs)
        return self.response


def _fake_client(parsed: LetterExtraction | None, stop_reason: str = "end_turn") -> Any:
    response = SimpleNamespace(
        stop_reason=stop_reason,
        parsed_output=parsed,
        usage=SimpleNamespace(input_tokens=2000, output_tokens=300),
    )
    return SimpleNamespace(messages=FakeMessages(response))


def test_successful_extraction(sample_pdf: Path, sample_label: LetterExtraction) -> None:
    client = _fake_client(sample_label)
    extractor = ClaudeExtractor(model="claude-opus-5-5", client=client)

    result = extractor.extract(load_document(sample_pdf))

    assert result.error is None
    assert result.extraction == sample_label
    assert result.cost_usd == pytest.approx((2000 * 4 + 300 * 20) / 1e6)
    request = client.messages.calls[0]
    assert request["output_format"] is LetterExtraction
    assert request["messages"][0]["content"][0]["type"] == "document"


def test_truncated_output_is_an_error(sample_pdf: Path) -> None:
    client = _fake_client(None, stop_reason="max_tokens")
    result = ClaudeExtractor(model="claude-opus-5-5", client=client).extract(
        load_document(sample_pdf)
    )
    assert result.extraction is None
    assert result.error == "stop_reason=max_tokens"
