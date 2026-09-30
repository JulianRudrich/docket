# 2. Private documents never enter the repository

Date: 2026-09-30 · Status: accepted

## Context

The dataset consists of real administrative letters. They contain names,
addresses, tax numbers and bank details. The repository is intended to become
public.

## Decision

- `data/raw/`, `data/labels/` and `results/` are gitignored.
- Only synthetic samples (`data/samples/`) and document ids (`data/splits.json`)
  are committed.
- Published results are aggregated metrics and hand-picked, anonymized error
  examples.

## Consequences

- Others cannot reproduce the numbers without their own data. The synthetic
  sample keeps the pipeline and tests runnable for everyone.
- Sending documents to an external API is a processing of personal data. Only
  letters that I am allowed to use are included (see data/README.md).
