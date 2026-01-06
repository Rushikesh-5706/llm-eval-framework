from llm_eval.utils.silence import silence_absl
silence_absl()
from typing import Dict, List

from llm_eval.core.dataset import load_dataset
from llm_eval.core.metric_factory import create
from llm_eval.config.validator import (
    validate_dataset_sample,
    validate_metrics,
    validate_judge_config,
)
from llm_eval.judge.client import create_judge_client
from llm_eval.judge.judge import LLMJudge


def run_evaluation(
    dataset_path: str,
    model_outputs: Dict[str, Dict[int, str]],
    metrics: List[str],
    judge_config=None,
    judge_override=None,
):
    # 🔴 FAIL FAST
    validate_metrics(metrics)
    validate_judge_config(judge_config)

    dataset = load_dataset(dataset_path)
    results = []

    judge = None
    if judge_override is not None:
        judge = judge_override
    elif judge_config is not None:
        try:
            client = create_judge_client(judge_config.provider)
            judge = LLMJudge(client, judge_config)
        except Exception:
            print("⚠️ Judge disabled: API key not set")
            judge = None

    for idx, sample in enumerate(dataset):
        validate_dataset_sample(sample, idx)

        for model_name, outputs in model_outputs.items():
            record = {
                "model": model_name,
                "query": sample["query"],
                "answer": outputs.get(idx, ""),
                "expected_answer": sample["expected_answer"],
                "retrieved_contexts": sample["retrieved_contexts"],
                "scores": {},
            }

            for metric_name in metrics:
                metric = create(metric_name)
                record["scores"][metric_name.lower()] = metric.compute(record)

            if judge:
                try:
                    # Preferred: RAG-aware judge
                    judge_scores = judge.evaluate(
                        record["query"],
                        record["answer"],
                        record["retrieved_contexts"],
                    )
                except TypeError:
                    # Fallback: DummyJudge
                    judge_scores = judge.evaluate(
                        record["query"],
                        record["answer"],
                    )

                record["scores"]["llm_judge"] = judge_scores

            results.append(record)

    return results
