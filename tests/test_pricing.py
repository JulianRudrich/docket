import pytest

from docket.pricing import cost_usd


def test_known_model() -> None:
    assert cost_usd("claude-haiku-4-5", 1_000_000, 1_000_000) == pytest.approx(6.0)


def test_unknown_model_has_no_cost() -> None:
    assert cost_usd("my-finetuned-model", 1000, 1000) is None
