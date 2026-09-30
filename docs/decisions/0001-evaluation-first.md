# 1. Build the evaluation before the system

Date: 2026-09-30 · Status: accepted

## Context

An extraction pipeline can be built in an afternoon. Knowing whether it works,
and whether a change made it better, takes a labeled dataset and a scoring
method. Without them, every improvement is a guess based on a few examples.

## Decision

The labeled dataset and the evaluation harness come first (weeks 1–2). Every
later change to prompts, models or the pipeline is judged by its effect on the
`dev` metrics.

Running models and scoring predictions are separate commands, so predictions
can be re-scored for free when the metrics change.

## Consequences

- Early weeks produce no visible features, only data and numbers.
- All results are reproducible from a run directory.
- Comparing a fine-tuned small model with API models is a fair comparison on the
  same documents and the same metrics.
