from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable, List, Dict, Any, Optional

import pandas as pd


def ensure_directories(paths: Iterable[Path]) -> None:
	for p in paths:
		Path(p).mkdir(parents=True, exist_ok=True)


def resolve_path(path: Path) -> Path:
	p = Path(path)
	if not p.exists():
		raise FileNotFoundError(str(p))
	return p


def load_dataset(path: Path, limit: Optional[int] = None) -> List[Dict[str, Any]]:
	path = Path(path)
	ext = path.suffix.lower()
	if ext == ".csv":
		df = pd.read_csv(path)
		records = df.to_dict(orient="records")
	elif ext == ".json":
		obj = json.loads(path.read_text(encoding="utf-8"))
		if isinstance(obj, dict) and "data" in obj and isinstance(obj["data"], list):
			records = list(obj["data"])
		elif isinstance(obj, list):
			records = obj
		else:
			raise ValueError("Unsupported JSON dataset structure")
	else:
		raise ValueError(f"Unsupported dataset format: {ext}")
	if limit is not None:
		return records[: int(limit)]
	return records


def save_annotations_json(path: Path, annotations: Dict[str, Any]) -> None:
	Path(path).parent.mkdir(parents=True, exist_ok=True)
	Path(path).write_text(json.dumps(annotations, ensure_ascii=False, indent=2), encoding="utf-8")


def save_annotations_csv(path: Path, items: List[Dict[str, Any]]) -> None:
	# Flatten payload
	flat_rows: List[Dict[str, Any]] = []
	for item in items:
		row: Dict[str, Any] = {"id": item.get("id")}
		payload = item.get("payload", {})
		for key, value in payload.items():
			row[key] = value
		flat_rows.append(row)
	Path(path).parent.mkdir(parents=True, exist_ok=True)
	if not flat_rows:
		Path(path).write_text("")
		return
	fieldnames = sorted({k for row in flat_rows for k in row.keys()})
	with Path(path).open("w", newline="", encoding="utf-8") as f:
		writer = csv.DictWriter(f, fieldnames=fieldnames)
		writer.writeheader()
		for row in flat_rows:
			writer.writerow(row)
