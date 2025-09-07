from __future__ import annotations

import hashlib
import random
from typing import Dict, Any, List


def _deterministic_label(text: str, seed: int) -> str:
	# Deterministic label based on seeded hashing of text
	rng = random.Random(seed)
	# Mix seed and text into a stable digest
	digest = hashlib.sha256((str(seed) + "::" + (text or "")).encode("utf-8")).hexdigest()
	labels = ["NEGATIVE", "NEUTRAL", "POSITIVE"]
	index = int(digest[:8], 16) % len(labels)
	# shuffle labels with rng to make seed impactful beyond digest
	rng.shuffle(labels)
	return labels[index]


def annotate_records(records: List[Dict[str, Any]], label_field: str = "label", text_field: str = "text", seed: int = 0) -> Dict[str, Any]:
	items: List[Dict[str, Any]] = []
	for idx, rec in enumerate(records):
		text_val = str(rec.get(text_field, ""))
		label_val = _deterministic_label(text_val, seed=seed)
		items.append(
			{
				"id": rec.get("id", idx),
				"payload": {
					"text": text_val,
					label_field: label_val,
				},
				"meta": {
					"source": "annotatorx.simple_labeler",
					"seed": seed,
				},
			}
		)
	return {
		"version": 1,
		"items": items,
	}
