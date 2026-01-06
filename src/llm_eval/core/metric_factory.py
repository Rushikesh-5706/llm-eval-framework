from typing import Dict, Type
from llm_eval.core.base_metric import BaseMetric

REGISTRY: Dict[str, Type[BaseMetric]] = {}

def register(name: str):
    def wrapper(cls):
        REGISTRY[name.lower()] = cls
        return cls
    return wrapper


# ---- BUILT-IN METRICS ----
from llm_eval.metrics.reference import (
    BLEUMetric,
    RougeLMetric,
    BERTScoreMetric,
)

register("bleu")(BLEUMetric)
register("rouge_l")(RougeLMetric)
register("bertscore")(BERTScoreMetric)


# ---- RAG METRICS ----
from llm_eval.rag.metrics import (
    FaithfulnessMetric,
    ContextRelevancyMetric,
    AnswerRelevancyMetric,
)

register("faithfulness")(FaithfulnessMetric)
register("context_relevancy")(ContextRelevancyMetric)
register("answer_relevancy")(AnswerRelevancyMetric)


# ---- PLUGIN DISCOVERY ----
def discover_plugins():
    try:
        import llm_eval.plugins  # noqa
    except Exception:
        pass


def create(name: str) -> BaseMetric:
    discover_plugins()
    key = name.lower()
    if key not in REGISTRY:
        raise ValueError(f"Metric not found: {name}")
    return REGISTRY[key]()

