from llm_eval.core.metric_factory import create


def test_plugin_metric_loaded():
    metric = create("length")
    score = metric.compute({"answer": "abcd"})
    assert score == 4.0
