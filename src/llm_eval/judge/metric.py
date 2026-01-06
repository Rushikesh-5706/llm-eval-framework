from llm_eval.core.base_metric import BaseMetric
import inspect

class JudgeMetric(BaseMetric):
    name = "llm_judge"

    def __init__(self, judge):
        self.judge = judge

    def compute(self, record):
        sig = inspect.signature(self.judge.evaluate)
        params = len(sig.parameters)

        if params == 2:
            # DummyJudge: evaluate(query, answer)
            return self.judge.evaluate(
                record["query"],
                record["answer"],
            )

        elif params == 3:
            # Real Judge: evaluate(query, answer, contexts)
            return self.judge.evaluate(
                record["query"],
                record["answer"],
                record.get("retrieved_contexts", []),
            )

        else:
            raise RuntimeError(
                f"Unsupported judge.evaluate signature: {sig}"
            )
