from llm_eval.judge.metric import JudgeMetric

class DummyJudge:
    def evaluate(self, query, answer):
        return {
            "coherence": 0.9,
            "relevance": 0.8,
            "safety": 1.0
        }

def test_judge_metric():
    metric = JudgeMetric(DummyJudge())
    sample = {"query": "test", "answer": "test"}
    scores = metric.compute(sample)

    assert scores["coherence"] == 0.9
    assert scores["relevance"] == 0.8
    assert scores["safety"] == 1.0
