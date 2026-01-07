# LLM Evaluation Framework – API Documentation

## Core Interfaces

### BaseMetric
**Location:** `llm_eval/core/base_metric.py`

Abstract base class for all metrics.

**Key Method:**
- `compute(record: dict) -> float`

All metrics must implement this interface.

---

## Evaluation Engine

### run_evaluation
**Location:** `llm_eval/core/evaluator.py`

Runs evaluation across dataset, models, and metrics.

**Parameters:**
- `dataset_path: str`
- `model_outputs: Dict[str, Dict[int, str]]`
- `metrics: List[str]`
- `judge_config: Optional[dict]`

**Returns:**
- List of per-example result dictionaries

---

## Dataset Loader

### load_dataset
**Location:** `llm_eval/core/dataset.py`

Loads JSONL or CSV datasets and validates required fields.

Required fields:
- `query`
- `expected_answer`
- `retrieved_contexts`

---

## Reporting

### aggregate
**Location:** `llm_eval/reporting/aggregate.py`

Computes aggregate statistics:
- Mean
- Median
- Standard deviation
- Min / Max

---

### write_json
**Location:** `llm_eval/reporting/writers.py`

Writes structured evaluation results to JSON.

---

### write_markdown
**Location:** `llm_eval/reporting/writers.py`

Generates human-readable Markdown reports.

---

## Visualization

### plot_histograms
**Location:** `llm_eval/visualization/plots.py`

Generates histogram PNGs for each metric.

---

### plot_radar
**Location:** `llm_eval/visualization/plots.py`

Generates a radar chart comparing aggregate metric performance.

---

## CLI

### llm-eval
**Location:** `llm_eval/cli/main.py`

Command-line interface.

**Options:**
- `--config`
- `--output-dir`
- `--models`
- `--metrics`
- `--verbose`

Designed for automation and CI/CD execution.
