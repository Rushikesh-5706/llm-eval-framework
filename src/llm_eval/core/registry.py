from typing import Dict, Type
from llm_eval.core.base_metric import BaseMetric

REGISTRY: Dict[str, Type[BaseMetric]] = {}


def register(name: str):
    def wrapper(cls):
        REGISTRY[name.lower()] = cls
        return cls
    return wrapper

