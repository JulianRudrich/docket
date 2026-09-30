# Data

Real administrative letters contain names, addresses, tax IDs and bank details.
This directory is organized so that none of that can end up on GitHub by accident.

```
data/
├── raw/          # original PDFs/scans            (gitignored)
├── labels/       # gold labels, one JSON per doc  (gitignored)
├── samples/      # synthetic letters + labels     (committed)
└── splits.json   # doc ids per split              (committed, ids only)
```

## Collecting documents

1. Scan or save the letter as PDF (or PNG/JPG for phone photos).
2. Name it with a neutral, sequential id: `letter_0001.pdf`, `letter_0002.pdf`, ...
   Never put names, authorities or dates into file names.
3. Keep a private note of where each letter came from, outside this repository.
4. Only use letters you are allowed to use: your own, or with the explicit consent
   of the person they are addressed to.

Aim for variety over volume: different authorities, letter types, layouts, scans
and photos. 150 to 300 documents is enough for this project.

## Labeling

Follow [docs/labeling-guide.md](../docs/labeling-guide.md). Every label must pass:

```bash
uv run bescheid validate-labels
```

## Splits

`splits.json` assigns every document to exactly one split:

| Split | Share | Used for |
|---|---|---|
| `train` | ~60% | fine-tuning data (week 4) |
| `dev` | ~20% | prompt iteration, error analysis, model comparison |
| `test` | ~20% | final numbers only, looked at as rarely as possible |

Split by **source**, not randomly by document: if several letters come from the
same authority and person, keep them in the same split. Otherwise the model can
memorize layouts and the test score overstates real performance.

## Publishing

Nothing from `raw/` or `labels/` is published. If a public dataset is released
later, it will be a separate, fully anonymized subset where every personal value
is replaced by a synthetic one of the same format.
