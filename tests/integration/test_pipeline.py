from llm_eval.core.evaluator import run_evaluation

def test_pipeline_runs(tmp_path):
    dataset = "benchmarks/rag_benchmark.jsonl"
    models = {
        "test": {i: "dummy answer" for i in range(25)}
    }
    metrics = ["bleu"]

    results = run_evaluation(dataset, models, metrics)
    assert len(results) == 25
