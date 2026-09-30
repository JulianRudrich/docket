"""Running an extractor over a dataset split and storing the raw predictions.

Running and scoring are separate steps: API calls cost money, scoring is free.
A run directory can be re-scored any number of times after the metrics change.

results/<run_id>/
    run.json            configuration, git commit, totals
    predictions.jsonl   one ExtractionResult per line
    metrics.json        written by `docket score`
"""

from __future__ import annotations

import json
import subprocess
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

from docket.dataset import Example
from docket.documents import load_document
from docket.extractors.base import ExtractionResult, Extractor


def git_commit() -> str | None:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=True
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return out.stdout.strip()


def run_extraction(
    extractor: Extractor,
    examples: list[Example],
    results_dir: Path,
    *,
    split: str,
    prompt_version: str,
    on_result: Callable[[ExtractionResult], None] | None = None,
) -> Path:
    started = datetime.now(UTC)
    run_id = f"{started:%Y%m%d-%H%M%S}_{extractor.model}_{split}"
    run_dir = results_dir / run_id
    run_dir.mkdir(parents=True)

    results: list[ExtractionResult] = []
    with (run_dir / "predictions.jsonl").open("w", encoding="utf-8") as f:
        for example in examples:
            result = extractor.extract(load_document(example.document_path))
            f.write(result.model_dump_json() + "\n")
            f.flush()
            results.append(result)
            if on_result:
                on_result(result)

    costs = [r.cost_usd for r in results if r.cost_usd is not None]
    run_info = {
        "run_id": run_id,
        "model": extractor.model,
        "split": split,
        "prompt_version": prompt_version,
        "git_commit": git_commit(),
        "started_at": started.isoformat(),
        "n_documents": len(results),
        "n_errors": sum(r.error is not None for r in results),
        "total_cost_usd": sum(costs) if costs else None,
        "mean_latency_s": sum(r.latency_s for r in results) / len(results) if results else None,
    }
    (run_dir / "run.json").write_text(json.dumps(run_info, indent=2), encoding="utf-8")
    return run_dir


def load_predictions(run_dir: Path) -> list[ExtractionResult]:
    lines = (run_dir / "predictions.jsonl").read_text(encoding="utf-8").splitlines()
    return [ExtractionResult.model_validate_json(line) for line in lines if line.strip()]
