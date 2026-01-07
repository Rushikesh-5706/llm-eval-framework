# Architecture Overview – LLM Evaluation Framework

This document describes the internal architecture and design principles of the LLM Evaluation Framework.

---

## High-Level Architecture

The system follows a modular, layered architecture designed for extensibility, testability, and production use.

```
CLI
 │
 ▼
Configuration Loader
 │
 ▼
Evaluation Engine
 │
 ├── Metric Factory
 │   ├── Reference Metrics
 │   ├── RAG Metrics
 │   └── Judge Metrics
 │
 ├── Dataset Loader
 │
 └── Result Aggregator
 │
 ▼
Reporting & Visualization
```

---

## Core Components

### CLI Layer
- Entry point: `llm-eval`
- Parses arguments (config, output-dir, metrics, models, verbose)
- Orchestrates full evaluation run

---

### Configuration System
- Supports YAML and JSON
- Validated using schema models
- Resolves dataset paths, model outputs, metrics, and judge settings

---

### Dataset Loader
- Supports JSONL and CSV formats
- Validates required fields:
  - query
  - expected_answer
  - retrieved_contexts
- Fails fast on malformed data

---

### Metric Architecture

All metrics inherit from a shared BaseMetric interface:

- `compute(record) -> float`

Metric categories:

#### Reference Metrics
- BLEU
- ROUGE-L
- BERTScore

#### RAG Metrics
- Faithfulness
- Context Relevancy
- Answer Relevancy

#### LLM-as-a-Judge
- Multi-dimensional rubric
- Coherence
- Relevance
- Safety
- Retry and backoff support

Metrics are registered via a factory pattern, enabling plugin-based extension.

---

### Evaluation Engine

Responsibilities:
- Iterate dataset samples
- Evaluate multiple models per sample
- Execute all configured metrics
- Capture per-example scores and errors

---

### Aggregation Layer

Calculates:
- Mean
- Median
- Standard deviation
- Min / Max

Aggregated per metric across dataset.

---

### Reporting

Outputs:
- Machine-readable JSON (`results.json`)
- Human-readable Markdown (`report.md`)

---

### Visualization

Generated using matplotlib:
- Histogram per metric
- Radar chart comparing aggregate scores

Saved as PNG files for CI and documentation use.

---

## Containerization

- Dockerfile defines Python 3.9 runtime
- docker-compose enables one-command execution
- Volumes mounted for benchmarks, examples, and results

---

## CI/CD Design

GitHub Actions workflow:
- Installs dependencies with Poetry
- Runs test suite
- Executes evaluation
- Uploads artifacts

---

## Design Principles

- Separation of concerns
- Fail-fast validation
- Extensibility without core modification
- Deterministic, reproducible evaluation
- Production-first engineering

---

## Conclusion

This architecture enables reliable, automated evaluation of LLM systems and reflects production-grade software engineering practices suitable for real-world AI deployments.

