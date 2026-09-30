from pathlib import Path

import pytest

from bescheid.documents import load_document, pdf_text


def test_load_pdf(sample_pdf: Path) -> None:
    document = load_document(sample_pdf)
    assert document.doc_id == "synthetic_mahnung_001"
    assert document.is_pdf


def test_pdf_text_contains_letter_content(sample_pdf: Path) -> None:
    text = pdf_text(load_document(sample_pdf))
    assert "Kassenzeichen" in text
    assert "101,50 EUR" in text


def test_unsupported_file_type(tmp_path: Path) -> None:
    path = tmp_path / "letter.docx"
    path.write_bytes(b"")
    with pytest.raises(ValueError, match="Unsupported file type"):
        load_document(path)
