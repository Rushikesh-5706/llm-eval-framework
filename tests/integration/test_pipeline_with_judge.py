from llm_eval.core.evaluator import run_evaluation

class DummyJudge:
    def evaluate(self, query, answer):
        return {"coherence": 1.0, "relevance": 1.0, "safety": 1.0}

def test_pipeline_with_judge(tmp_path):
    dataset = tmp_path / "data.jsonl"
    dataset.write_text(
        '{"query":"q","expected_answer":"a","retrieved_contexts":["a"]}\n'
    )

    outputs = {"m": {0: "a"}}

    results = run_evaluation(
        str(dataset),
        outputs,
        ["bleu"],
        judge_override=DummyJudge()
    )

    assert "llm_judge" in results[0]["scores"]
    assert results[0]["scores"]["llm_judge"]["coherence"] == 1.0
