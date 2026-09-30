"""Command line interface: `uv run docket --help`."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError
from rich.console import Console
from rich.table import Table

from docket.config import get_settings
from docket.dataset import SPLITS, load_label, load_split
from docket.documents import load_document
from docket.evaluation.runner import load_predictions, run_extraction
from docket.extractors import ExtractionResult, get_extractor
from docket.schema import LetterExtraction

app = typer.Typer(no_args_is_help=True, help="Structured extraction from German official letters.")
console = Console()

ModelOption = Annotated[str | None, typer.Option(help="Model name (default: DOCKET_MODEL).")]


@app.command()
def extract(path: Path, model: ModelOption = None) -> None:
    """Extract one document and print the result as JSON."""
    settings = get_settings()
    extractor = get_extractor(model or settings.model, settings.prompt_version)
    result = extractor.extract(load_document(path))
    if result.extraction is None:
        console.print(f"[red]Extraction failed:[/red] {result.error}")
        raise typer.Exit(1)
    console.print_json(result.extraction.model_dump_json())
    cost = f"${result.cost_usd:.4f}" if result.cost_usd is not None else "n/a"
    console.print(
        f"[dim]{result.model} · {result.input_tokens} in / {result.output_tokens} out tokens"
        f" · {result.latency_s:.1f}s · {cost}[/dim]"
    )


@app.command("validate-labels")
def validate_labels() -> None:
    """Check that every label file matches the schema."""
    labels_dir = get_settings().labels_dir
    paths = sorted(labels_dir.glob("*.json"))
    failures = 0
    for path in paths:
        try:
            load_label(path)
        except ValidationError as exc:
            failures += 1
            console.print(f"[red]✗ {path.name}[/red]\n{exc}")
    console.print(f"{len(paths) - failures}/{len(paths)} labels valid")
    if failures:
        raise typer.Exit(1)


@app.command()
def run(
    split: Annotated[str, typer.Option(help=f"One of {', '.join(SPLITS)}.")] = "dev",
    model: ModelOption = None,
) -> None:
    """Run a model over a dataset split and store its predictions."""
    if split == "test":
        typer.confirm(
            "The test split is for final numbers only. Every look at it leaks information "
            "into your decisions. Continue?",
            abort=True,
        )
    settings = get_settings()
    examples = load_split(settings.data_dir, split)
    extractor = get_extractor(model or settings.model, settings.prompt_version)

    def report(result: ExtractionResult) -> None:
        status = "[green]✓[/green]" if result.error is None else f"[red]✗ {result.error}[/red]"
        console.print(f"{status} {result.doc_id} ({result.latency_s:.1f}s)")

    run_dir = run_extraction(
        extractor,
        examples,
        settings.results_dir,
        split=split,
        prompt_version=settings.prompt_version,
        on_result=report,
    )
    console.print(f"Predictions written to {run_dir}. Next: uv run docket score {run_dir}")


@app.command()
def score(run_dir: Path) -> None:
    """Score the predictions of a run against the gold labels."""
    from docket.evaluation.metrics import aggregate, score_document

    settings = get_settings()
    scores = []
    for result in load_predictions(run_dir):
        gold = load_label(settings.labels_dir / f"{result.doc_id}.json")
        scores.append(score_document(result.doc_id, result.extraction, gold))
    metrics = aggregate(scores)
    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    table = Table(title=run_dir.name)
    table.add_column("metric")
    table.add_column("value", justify="right")
    for name, value in metrics.items():
        table.add_row(name, f"{value:.3f}")
    console.print(table)


@app.command("schema")
def print_schema() -> None:
    """Print the JSON schema that labels and model outputs must follow."""
    console.print_json(json.dumps(LetterExtraction.model_json_schema()))
