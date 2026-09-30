from pathlib import Path

import pytest

from docket.dataset import load_label
from docket.schema import LetterExtraction

SAMPLES = Path(__file__).resolve().parent.parent / "data" / "samples"


@pytest.fixture
def sample_pdf() -> Path:
    return SAMPLES / "synthetic_mahnung_001.pdf"


@pytest.fixture
def sample_label() -> LetterExtraction:
    return load_label(SAMPLES / "synthetic_mahnung_001.json")
