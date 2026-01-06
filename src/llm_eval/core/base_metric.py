from abc import ABC, abstractmethod
from typing import Dict

class BaseMetric(ABC):
    name: str

    @abstractmethod
    def compute(self, record: Dict):
        raise NotImplementedError


# Backward compatibility (do NOT remove)
Metric = BaseMetric
