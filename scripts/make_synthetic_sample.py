"""Render the synthetic sample letter in data/samples/ as a PDF.

The sample is fictional (no real person, authority or account) and exists so
that the pipeline, the tests and the README demo work without private data.

    uv run python scripts/make_synthetic_sample.py
"""

from pathlib import Path

import pymupdf

SAMPLES = Path(__file__).resolve().parent.parent / "data" / "samples"

LETTER = """\
Stadt Musterstadt · Stadtkasse · Rathausplatz 1 · 12345 Musterstadt

Frau
Erika Beispiel
Lindenweg 7
12345 Musterstadt
                                                                                    Musterstadt, 14.09.2026
                                                                         Kassenzeichen: 5.0412.778.3

Mahnung – Hundesteuer 2026

Sehr geehrte Frau Beispiel,

nach unseren Unterlagen ist die folgende Forderung trotz Fälligkeit noch nicht beglichen:

    Hundesteuer 2026, 3. Quartal                      96,50 EUR
    Mahngebühr gem. § 19 VwVG                          5,00 EUR
    ---------------------------------------------------------------
    Gesamtbetrag                                     101,50 EUR

Bitte überweisen Sie den Gesamtbetrag bis spätestens 28.09.2026 unter Angabe des
Kassenzeichens 5.0412.778.3 auf folgendes Konto:

    Empfänger: Stadtkasse Musterstadt
    IBAN: DE02 1203 0000 0000 2020 51

Sollte der Betrag bis zu diesem Datum nicht eingegangen sein, müssen wir ohne
weitere Ankündigung die Zwangsvollstreckung einleiten. Hierdurch entstehen Ihnen
weitere Kosten.

Haben Sie die Zahlung bereits geleistet, betrachten Sie dieses Schreiben bitte
als gegenstandslos.

Mit freundlichen Grüßen
Im Auftrag

Müller
"""


def main() -> None:
    SAMPLES.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)  # A4 in points
    page.insert_textbox(pymupdf.Rect(60, 60, 540, 800), LETTER, fontsize=9.5, fontname="cour")
    out = SAMPLES / "synthetic_mahnung_001.pdf"
    doc.save(out, deflate=True)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
