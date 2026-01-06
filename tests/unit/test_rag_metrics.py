from llm_eval.rag.metrics import (
    FaithfulnessMetric,
    ContextRelevancyMetric,
    AnswerRelevancyMetric,
)

def test_faithfulness_metric():
    metric = FaithfulnessMetric()
    sample = {
        "answer": "Paris is the capital of France",
        "retrieved_contexts": ["Paris is the capital of France"]
    }
    assert metric.compute(sample) == 1.0

def test_context_relevancy_metric():
    metric = ContextRelevancyMetric()
    sample = {
        "query": "What is the capital of France?",
        "retrieved_contexts": ["Paris is the capital of France"]
    }
    assert metric.compute(sample) > 0.5

def test_answer_relevancy_metric():
    metric = AnswerRelevancyMetric()
    sample = {
        "query": "What is the capital of France?",
        "answer": "Paris is the capital of France"
    }
    assert metric.compute(sample) > 0.5

def test_faithfulness_metric():
    from llm_eval.rag.metrics import FaithfulnessMetric

    metric = FaithfulnessMetric()

    grounded = {
        "answer": "Paris is the capital of France",
        "retrieved_contexts": ["Paris is the capital of France"]
    }

    hallucinated = {
        "answer": "Paris is the capital of Germany",
        "retrieved_contexts": ["Paris is the capital of France"]
    }

    assert metric.compute(grounded) > 0.9
    assert metric.compute(hallucinated) < 0.8
