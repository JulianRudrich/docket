import json
from pathlib import Path

import pytest

from docket.dataset import load_split, load_splits


def _write_dataset(root: Path, sample_pdf: Path, label_json: str) -> None:
    (root / "raw").mkdir()
    (root / "labels").mkdir()
    (root / "raw" / "doc1.pdf").write_bytes(sample_pdf.read_bytes())
    (root / "labels" / "doc1.json").write_text(label_json, encoding="utf-8")
    splits = {"train": [], "dev": ["doc1"], "test": []}
    (root / "splits.json").write_text(json.dumps(splits), encoding="utf-8")


def test_load_split(tmp_path: Path, sample_pdf: Path) -> None:
    label = (sample_pdf.with_suffix(".json")).read_text(encoding="utf-8")
    _write_dataset(tmp_path, sample_pdf, label)
    examples = load_split(tmp_path, "dev")
    assert [e.doc_id for e in examples] == ["doc1"]
    assert examples[0].document_path.suffix == ".pdf"


def test_document_in_two_splits_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "splits.json"
    path.write_text(json.dumps({"train": ["a"], "test": ["a"]}), encoding="utf-8")
    with pytest.raises(ValueError, match="both"):
        load_splits(path)
