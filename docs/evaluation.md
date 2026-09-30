# Evaluation

How models are compared in this project. The implementation lives in
[`src/docket/evaluation/`](../src/docket/evaluation/).

## Workflow

```bash
uv run docket run --split dev --model claude-opus-5-5   # costs money, stores predictions
uv run docket score results/<run_id>                    # free, can be repeated
```

Every run directory records the model, prompt version, git commit, cost and
latency, so every number in the README can be reproduced.

## What is measured

| Metric | Definition |
|---|---|
| `<field>_accuracy` | Share of documents where a scalar field is exactly right after normalization |
| `payments_precision/recall/f1` | Payment matching, micro-averaged over all documents |
| `deadlines_precision/recall/f1` | Deadline matching, micro-averaged over all documents |
| `document_exact` | Share of documents with **every** scored field and list item correct |
| cost per document | USD, from token usage and list prices |
| latency | Seconds per document, p50 and p95 |

`document_exact` is the headline metric: a letter is only useful to a user if
everything that matters is right.

## Matching rules

- A **payment** matches if amount (to the cent), due date and normalized IBAN
  are equal. `payment_reference` is reported separately.
- A **deadline** matches if kind and date are equal. `description` is not scored.
- A failed extraction counts as wrong on every field.

_TODO(week 2): record the normalization decisions for authority names here._

## Rules for honest numbers

1. Prompts and models are chosen on `dev`. `test` is only used for final numbers.
2. Every prompt change gets a new prompt version; results always name the version.
3. Error analysis is part of every result: which fields fail, and why.
