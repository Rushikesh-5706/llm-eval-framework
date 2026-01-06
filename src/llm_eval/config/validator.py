from typing import List

REQUIRED_DATASET_FIELDS = {"query", "expected_answer", "retrieved_contexts"}
REQUIRED_JUDGE_RUBRIC = {"coherence", "relevance", "safety"}


def validate_models(models: dict):
    if not isinstance(models, dict) or not models:
        raise ValueError("Config must contain at least one model output")


def validate_metrics(metrics: List[str]):
    if not metrics:
        raise ValueError("At least one metric must be specified")
    for m in metrics:
        if not isinstance(m, str):
            raise ValueError(f"Invalid metric name: {m}")


def validate_judge_config(judge_config):
    if judge_config is None:
        return
    rubric = judge_config.rubric
    missing = REQUIRED_JUDGE_RUBRIC - set(rubric.__dict__.keys())
    if missing:
        raise ValueError(f"Judge rubric missing required fields: {missing}")


def validate_dataset_sample(sample: dict, idx: int):
    missing = REQUIRED_DATASET_FIELDS - set(sample.keys())
    if missing:
        raise ValueError(
            f"Dataset sample {idx} missing required field(s): {sorted(missing)}"
        )
