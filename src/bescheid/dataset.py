"""Access to the labeled dataset.

Layout (see data/README.md):
    data/raw/<doc_id>.pdf|png|jpg   original documents, never committed
    data/labels/<doc_id>.json       gold labels (LetterExtraction)
    data/splits.json                {"train": [...], "dev": [...], "test": [...]}
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from bescheid.documents import MEDIA_TYPES
from bescheid.schema import LetterExtraction

SPLITS = ("train", "dev", "test")


@dataclass(frozen=True)
class Example:
    doc_id: str
    document_path: Path
    label: LetterExtraction


def load_label(path: Path) -> LetterExtraction:
    return LetterExtraction.model_validate_json(path.read_text(encoding="utf-8"))


def find_document(raw_dir: Path, doc_id: str) -> Path:
    for suffix in MEDIA_TYPES:
        candidate = raw_dir / f"{doc_id}{suffix}"
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"No document for {doc_id!r} in {raw_dir}")


def load_splits(splits_file: Path) -> dict[str, list[str]]:
    splits: dict[str, list[str]] = json.loads(splits_file.read_text(encoding="utf-8"))
    unknown = set(splits) - set(SPLITS)
    if unknown:
        raise ValueError(f"Unknown splits in {splits_file}: {sorted(unknown)}")
    seen: dict[str, str] = {}
    for split, doc_ids in splits.items():
        for doc_id in doc_ids:
            if doc_id in seen:
                raise ValueError(f"{doc_id!r} is in both {seen[doc_id]!r} and {split!r}")
            seen[doc_id] = split
    return splits


def load_split(data_dir: Path, split: str) -> list[Example]:
    doc_ids = load_splits(data_dir / "splits.json").get(split, [])
    return [
        Example(
            doc_id=doc_id,
            document_path=find_document(data_dir / "raw", doc_id),
            label=load_label(data_dir / "labels" / f"{doc_id}.json"),
        )
        for doc_id in doc_ids
    ]
