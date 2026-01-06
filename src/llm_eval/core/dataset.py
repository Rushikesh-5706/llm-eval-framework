import json
import csv
from pathlib import Path
from typing import List, Dict, Any


REQUIRED_FIELDS = {"query", "expected_answer", "retrieved_contexts"}


def load_dataset(path: str) -> List[Dict[str, Any]]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    rows: List[Dict[str, Any]] = []

    if p.suffix == ".jsonl":
        for line in p.read_text().splitlines():
            row = json.loads(line)
            _validate(row)
            rows.append(row)

    elif p.suffix == ".csv":
        with p.open() as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["retrieved_contexts"] = json.loads(row["retrieved_contexts"])
                _validate(row)
                rows.append(row)

    else:
        raise ValueError("Dataset must be JSONL or CSV")

    return rows


def _validate(row: Dict[str, Any]):
    missing = REQUIRED_FIELDS - row.keys()
    if missing:
        raise ValueError(f"Dataset row missing fields: {missing}")
