from llm_eval.metrics.reference import BLEUMetric, RougeLMetric

def test_bleu_basic():
    metric = BLEUMetric()
    sample = {
        "expected_answer": "hello world",
        "answer": "hello world"
    }
    assert metric.compute(sample) > 0.9

def test_rouge_basic():
    metric = RougeLMetric()
    sample = {
        "expected_answer": "hello world",
        "answer": "hello world"
    }
    assert metric.compute(sample) == 1.0
