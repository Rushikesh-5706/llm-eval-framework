from typing import Dict, Any, List
import re

from llm_eval.core.base_metric import Metric


class ContextRelevancyMetric(Metric):
    name = "context_relevancy"

    def compute(self, sample: Dict[str, Any]) -> float:
        query = sample.get("query", "")
        contexts = sample.get("retrieved_contexts", [])

        if not query or not contexts:
            return 0.0

        query_tokens = self._tokenize(query)
        context_text = " ".join(contexts).lower()

        if not query_tokens:
            return 0.0

        matched = sum(1 for t in query_tokens if t in context_text)
        return matched / len(query_tokens)

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        return re.findall(r"\b\w+\b", text.lower())


class AnswerRelevancyMetric(Metric):
    name = "answer_relevancy"

    def compute(self, sample: Dict[str, Any]) -> float:
        query = sample.get("query", "")
        answer = sample.get("answer", "")

        if not query or not answer:
            return 0.0

        query_tokens = self._tokenize(query)
        answer_text = answer.lower()

        if not query_tokens:
            return 0.0

        matched = sum(1 for t in query_tokens if t in answer_text)
        return matched / len(query_tokens)

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        return re.findall(r"\b\w+\b", text.lower())


class FaithfulnessMetric(Metric):
    """
    Measures whether the generated answer is grounded in the retrieved context.
    Penalizes hallucinated entities.
    """

    name = "faithfulness"

    def compute(self, sample: Dict[str, Any]) -> float:
        answer = sample.get("answer", "")
        contexts = sample.get("retrieved_contexts", [])

        if not answer or not contexts:
            return 0.0

        context_text = " ".join(contexts).lower()
        tokens = self._tokenize(answer)

        if not tokens:
            return 0.0

        grounded = sum(1 for t in tokens if t in context_text)
        return grounded / len(tokens)

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        stopwords = {"the", "is", "a", "an", "of", "and", "to", "in"}
        tokens = re.findall(r"\b\w+\b", text.lower())
        return [t for t in tokens if t not in stopwords]
