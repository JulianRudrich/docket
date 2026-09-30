"""Scoring model predictions against gold labels.

Implementing this module is Julian's task for week 2 (see issue "Implement
evaluation metrics"). The expected behavior is specified by the tests in
tests/test_metrics.py, which are marked xfail until the functions exist.

Scoring rules (keep in sync with docs/evaluation.md):
- Scalar fields (letter_type, issuing_authority, letter_date, reference_number,
  action_required, legal_remedy.kind, legal_remedy.period_months) are scored as
  correct / incorrect after normalization.
- `payments` and `deadlines` are lists: count true positives, false positives and
  false negatives, then report precision, recall and F1.
- `summary` is free text and is not scored automatically.
- A failed extraction (prediction is None) counts every field as wrong and
  every gold list item as a false negative.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from docket.schema import LetterExtraction

SCALAR_FIELDS = (
    "letter_type",
    "issuing_authority",
    "letter_date",
    "reference_number",
    "action_required",
    "legal_remedy_kind",
    "legal_remedy_period_months",
)


@dataclass
class MatchCounts:
    tp: int = 0
    fp: int = 0
    fn: int = 0

    @property
    def precision(self) -> float:
        return self.tp / (self.tp + self.fp) if self.tp + self.fp else 1.0

    @property
    def recall(self) -> float:
        return self.tp / (self.tp + self.fn) if self.tp + self.fn else 1.0

    @property
    def f1(self) -> float:
        p, r = self.precision, self.recall
        return 2 * p * r / (p + r) if p + r else 0.0


@dataclass
class DocumentScore:
    doc_id: str
    fields: dict[str, bool] = field(default_factory=dict)
    payments: MatchCounts = field(default_factory=MatchCounts)
    deadlines: MatchCounts = field(default_factory=MatchCounts)


def normalize_identifier(value: str | None) -> str | None:
    """Normalize IBANs and reference numbers: drop whitespace, uppercase.

    >>> normalize_identifier("DE89 3704 0044 0532 0130 00")
    'DE89370400440532013000'
    """
    if value is None:
        return None
    return re.sub(r"\s+", "", value).upper()


def normalize_name(value: str) -> str:
    """Normalize authority names for comparison.

    TODO(week 2): decide how lenient this should be. Is "Finanzamt Köln Mitte"
    the same as "Finanzamt Köln-Mitte"? Document the decision in docs/evaluation.md.
    """
    raise NotImplementedError


def score_document(
    doc_id: str, prediction: LetterExtraction | None, gold: LetterExtraction
) -> DocumentScore:
    """Score one prediction against its gold label. TODO(week 2)."""
    raise NotImplementedError


def aggregate(scores: list[DocumentScore]) -> dict[str, float]:
    """Combine document scores into dataset-level metrics. TODO(week 2).

    Expected keys: "<field>_accuracy" for every scalar field, "payments_precision",
    "payments_recall", "payments_f1", the same for deadlines, and "document_exact"
    (share of documents where every scalar field and every list item is correct).
    Sum MatchCounts across documents before computing precision/recall (micro-average).
    """
    raise NotImplementedError
