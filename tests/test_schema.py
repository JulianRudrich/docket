import pytest
from pydantic import ValidationError

from bescheid.schema import LetterExtraction, LetterType


def test_sample_label_is_valid(sample_label: LetterExtraction) -> None:
    assert sample_label.letter_type is LetterType.PAYMENT_REMINDER
    assert sample_label.payments[0].amount_eur == pytest.approx(101.5)


def test_unknown_fields_are_rejected(sample_label: LetterExtraction) -> None:
    data = sample_label.model_dump(mode="json") | {"confidence": 0.9}
    with pytest.raises(ValidationError):
        LetterExtraction.model_validate(data)


def test_json_schema_is_closed() -> None:
    """Structured outputs require additionalProperties: false on every object."""
    schema = LetterExtraction.model_json_schema()
    objects = [schema, *schema["$defs"].values()]
    for obj in objects:
        if obj.get("type") == "object":
            assert obj.get("additionalProperties") is False, obj.get("title")
