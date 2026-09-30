"""Loading input documents (PDFs and scans) from disk."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pymupdf

MEDIA_TYPES = {
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
}


@dataclass(frozen=True)
class Document:
    doc_id: str
    media_type: str
    data: bytes

    @property
    def is_pdf(self) -> bool:
        return self.media_type == "application/pdf"


def load_document(path: Path) -> Document:
    media_type = MEDIA_TYPES.get(path.suffix.lower())
    if media_type is None:
        supported = ", ".join(sorted(MEDIA_TYPES))
        raise ValueError(f"Unsupported file type {path.suffix!r} (supported: {supported})")
    return Document(doc_id=path.stem, media_type=media_type, data=path.read_bytes())


def pdf_text(document: Document) -> str:
    """Return the embedded text layer of a PDF.

    Scanned PDFs have no text layer and return an empty string; those need OCR
    before they can be fed to a text-only model.
    """
    if not document.is_pdf:
        raise ValueError(f"{document.doc_id} is not a PDF")
    with pymupdf.open(stream=document.data, filetype="pdf") as pdf:  # type: ignore[no-untyped-call]
        return "\n\n".join(page.get_text() for page in pdf).strip()
