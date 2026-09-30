"""Specification for docket.evaluation.metrics.

The xfail tests describe the behavior to implement in week 2. Once a function
works, its tests start passing and pytest reports them as XPASS(strict), which
fails the run: that is the reminder to delete the xfail marker.
"""

import pytest

from docket.evaluation.metrics import (
    MatchCounts,
    aggregate,
    normalize_identifier,
    normalize_name,
    score_document,
)
from docket.schema import LetterExtraction, LetterType

todo = pytest.mark.xfail(raises=NotImplementedError, reason="TODO(week 2)")


def test_normalize_identifier() -> None:
    assert normalize_identifier(" de02 1203 0000 ") == "DE0212030000"
    assert normalize_identifier(None) is None


def test_match_counts() -> None:
    counts = MatchCounts(tp=3, fp=1, fn=2)
    assert counts.precision == pytest.approx(0.75)
    assert counts.recall == pytest.approx(0.6)
    assert MatchCounts().f1 == pytest.approx(1.0)


@todo
def test_normalize_name_ignores_hyphens_and_case() -> None:
    assert normalize_name("Finanzamt Köln-Mitte") == normalize_name("finanzamt köln mitte")


@todo
def test_perfect_prediction(sample_label: LetterExtraction) -> None:
    score = score_document("doc", sample_label, sample_label)
    assert all(score.fields.values())
    assert score.payments == MatchCounts(tp=1, fp=0, fn=0)
    assert score.deadlines == MatchCounts(tp=1, fp=0, fn=0)


@todo
def test_failed_extraction_scores_zero(sample_label: LetterExtraction) -> None:
    score = score_document("doc", None, sample_label)
    assert not any(score.fields.values())
    assert score.payments == MatchCounts(tp=0, fp=0, fn=1)


@todo
def test_wrong_amount_is_false_positive_and_false_negative(
    sample_label: LetterExtraction,
) -> None:
    prediction = sample_label.model_copy(deep=True)
    prediction.payments[0].amount_eur = 96.5  # the item, not the total
    score = score_document("doc", prediction, sample_label)
    assert score.payments == MatchCounts(tp=0, fp=1, fn=1)


@todo
def test_iban_with_spaces_still_matches(sample_label: LetterExtraction) -> None:
    prediction = sample_label.model_copy(deep=True)
    prediction.payments[0].iban = "DE02 1203 0000 0000 2020 51"
    score = score_document("doc", prediction, sample_label)
    assert score.payments.tp == 1


@todo
def test_aggregate(sample_label: LetterExtraction) -> None:
    wrong_type = sample_label.model_copy(update={"letter_type": LetterType.FINE})
    scores = [
        score_document("a", sample_label, sample_label),
        score_document("b", wrong_type, sample_label),
    ]
    metrics = aggregate(scores)
    assert metrics["letter_type_accuracy"] == pytest.approx(0.5)
    assert metrics["payments_f1"] == pytest.approx(1.0)
    assert metrics["document_exact"] == pytest.approx(0.5)
