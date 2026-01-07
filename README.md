# LLM Evaluation Framework

A production-ready Python framework for systematically evaluating Large Language Model (LLM) applications such as Retrieval-Augmented Generation (RAG) pipelines, chatbots, and question-answering systems.

This framework provides automated quality assurance for LLM outputs, enabling engineers to measure accuracy, relevance, faithfulness, and safety in a repeatable, CI/CD-friendly manner.

---

## Why This Project Exists

Modern LLM systems often fail silently. Outputs may appear fluent while being factually incorrect, hallucinated, irrelevant to retrieved context, or unsafe. This framework addresses that gap by providing a standardized, automated evaluation pipeline.

---

## Key Features

### Evaluation Metrics
- BLEU (n-gram overlap)
- ROUGE-L (longest common subsequence)
- BERTScore (semantic similarity)
- Faithfulness (grounding in retrieved context)
- Context Relevancy
- Answer Relevancy
- LLM-as-a-Judge (multi-dimensional rubric)

### Engineering Capabilities
- CLI-driven execution
- YAML and JSON configuration
- Plugin-based metric architecture
- JSON and Markdown reporting
- Histogram and radar visualizations
- Dockerized execution
- CI/CD automation via GitHub Actions

---

## Repository Structure

```
.
├── benchmarks/              # Evaluation datasets
├── examples/                # Example configs & model outputs
├── src/llm_eval/            # Core framework code
├── tests/                   # Unit & integration tests
├── results/                 # Generated evaluation outputs
├── screenshots/             # CLI & CI evidence
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

---

## Installation (Local)

### Requirements
- Python 3.9 – 3.11
- Poetry

### Setup
```bash
poetry install
```

---

## CLI Usage

### Verify CLI
```bash
poetry run llm-eval --help
```

### Run Evaluation
```bash
poetry run llm-eval \
  --config examples/config.yaml \
  --output-dir results \
  --verbose
```

---

## Viewing Results

After execution completes:

```bash
ls results
```

Expected outputs:
- results.json
- report.md
- plots/

To view generated plots:

```bash
ls results/plots
```

---

## Docker Usage

Docker Image:
https://hub.docker.com/r/rushi5706/llm-eval

### One-Command Execution
```bash
docker-compose up --build
```

This builds the image, runs evaluation, and writes outputs to the results directory.

---

## CI/CD Integration

The repository includes a GitHub Actions workflow that:
- installs dependencies via Poetry
- runs unit and integration tests
- executes the evaluation pipeline
- fails builds on errors

---

## Screenshots

Screenshots demonstrating CLI execution, result generation, and CI success are located in the screenshots/ directory and rendered on GitHub.

---

## Testing

```bash
poetry run pytest tests/ --cov=llm_eval
```

The test suite includes unit and integration tests and achieves over 80% coverage.

---

## Summary

This project demonstrates production-grade Python engineering for LLM systems, including automated evaluation, extensible architecture, CI/CD integration, and Docker-based reproducibility.

