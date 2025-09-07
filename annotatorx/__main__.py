import json
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from .utils.io import (
	ensure_directories,
	load_dataset,
	save_annotations_json,
	save_annotations_csv,
	resolve_path,
)
from .pipeline.annotate import annotate_records
from .validators.schemas import AnnotationSet

console = Console()

DATASETS_DIR = Path("datasets")
ANNOTATIONS_DIR = Path("annotations")


@click.group(help="AnnotatorX CLI: ingest, annotate, validate, export, stats")
def cli() -> None:
	ensure_directories([DATASETS_DIR, ANNOTATIONS_DIR])


@cli.command()
@click.argument("file", type=click.Path(path_type=Path, exists=True))
@click.option("--name", "dataset_name", type=str, default=None, help="Optional dataset name to store as.")
@click.option("--format", "fmt", type=click.Choice(["csv", "json"]), default=None, help="Specify format if ambiguous")
def ingest(file: Path, dataset_name: Optional[str], fmt: Optional[str]) -> None:
	"""Import dataset (CSV/JSON) into datasets/ directory."""
	ensure_directories([DATASETS_DIR])
	source_path = resolve_path(file)
	if not dataset_name:
		dataset_name = source_path.stem
	if fmt is None:
		fmt = source_path.suffix.lstrip(".").lower()
	if fmt not in {"csv", "json"}:
		raise click.ClickException(f"Unsupported format: {fmt}")
	dest = DATASETS_DIR / f"{dataset_name}.{fmt}"
	dest.write_bytes(source_path.read_bytes())
	console.print(f"[green]Ingested[/green] {source_path} -> {dest}")


@cli.command()
@click.argument("dataset", type=str)
@click.option("--output", "output", type=click.Path(path_type=Path), default=ANNOTATIONS_DIR / "annotations.json")
@click.option("--label-field", type=str, default="label", help="Annotation label field name")
@click.option("--text-field", type=str, default="text", help="Input text field name")
@click.option("--seed", type=int, default=0, help="Seed for deterministic behavior")
@click.option("--limit", type=int, default=None, help="Limit number of rows to process")
def annotate(dataset: str, output: Path, label_field: str, text_field: str, seed: int, limit: Optional[int]) -> None:
	"""Apply simple annotation functions to a dataset and write JSON annotations."""
	path_csv = DATASETS_DIR / f"{dataset}.csv"
	path_json = DATASETS_DIR / f"{dataset}.json"
	dataset_path = path_csv if path_csv.exists() else path_json
	if not dataset_path.exists():
		raise click.ClickException(f"Dataset not found: {dataset} (.csv or .json)")

	records = load_dataset(dataset_path, limit=limit)
	annotations = annotate_records(records, label_field=label_field, text_field=text_field, seed=seed)

	save_annotations_json(output, annotations)
	console.print(f"[green]Annotated[/green] {len(annotations)} records -> {output}")


@cli.command()
@click.argument("annotations", type=click.Path(path_type=Path, exists=True))
def validate(annotations: Path) -> None:
	"""Validate annotation JSON against schema using Pydantic."""
	data = json.loads(Path(annotations).read_text(encoding="utf-8"))
	try:
		AnnotationSet.model_validate(data)
		console.print("[green]Validation passed[/green]")
	except Exception as exc:
		console.print(f"[red]Validation failed[/red]: {exc}")
		raise click.Abort()


@cli.command()
@click.argument("annotations", type=click.Path(path_type=Path, exists=True))
@click.option("--format", "fmt", type=click.Choice(["csv", "json"]), default="csv")
@click.option("--output", type=click.Path(path_type=Path), default=None)
def export(annotations: Path, fmt: str, output: Optional[Path]) -> None:
	"""Export annotations to CSV or JSON."""
	data = json.loads(Path(annotations).read_text(encoding="utf-8"))
	ann = AnnotationSet.model_validate(data)
	if fmt == "json":
		out = output or (Path(annotations).with_suffix(".export.json"))
		save_annotations_json(out, ann.model_dump())
	else:
		out = output or (Path(annotations).with_suffix(".csv"))
		save_annotations_csv(out, ann.items)
	console.print(f"[green]Exported[/green] {fmt.upper()} -> {out}\n")


@cli.command()
@click.argument("annotations", type=click.Path(path_type=Path, exists=True))
def stats(annotations: Path) -> None:
	"""Show summary metrics for annotations."""
	data = json.loads(Path(annotations).read_text(encoding="utf-8"))
	ann = AnnotationSet.model_validate(data)

	# Count labels
	counts = {}
	for item in ann.items:
		label = item.payload.get("label")
		counts[label] = counts.get(label, 0) + 1

	table = Table(title="Annotation Label Distribution")
	table.add_column("Label")
	table.add_column("Count", justify="right")
	for label, count in sorted(counts.items(), key=lambda kv: (str(kv[0]), kv[1])):
		table.add_row(str(label), str(count))
	table.add_row("TOTAL", str(len(ann.items)))
	console.print(table)


if __name__ == "__main__":
	try:
		cli(prog_name="annotatorx")
	except click.Abort:
		sys.exit(1)
