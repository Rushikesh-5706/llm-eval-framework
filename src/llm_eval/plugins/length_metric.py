from llm_eval.core.base_metric import BaseMetric
from llm_eval.core.metric_factory import register

@register("length")
class LengthMetric(BaseMetric):
    def compute(self, record):
        return len(record.get("answer", ""))
