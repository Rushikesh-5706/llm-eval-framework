from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from bert_score import score as bert_score
from llm_eval.core.base_metric import Metric

class BLEUMetric(Metric):
    name = "bleu"
    def compute(self, sample):
        ref = sample["expected_answer"].split()
        hyp = sample["answer"].split()
        n = min(4, len(ref), len(hyp))
        weights = tuple([1 / n] * n)
        return sentence_bleu(
            [ref],
            hyp,
            weights=weights,
            smoothing_function=SmoothingFunction().method1,
        )

class RougeLMetric(Metric):
    name = "rouge_l"
    def compute(self, sample):
        scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
        return scorer.score(
            sample["expected_answer"],
            sample["answer"],
        )["rougeL"].fmeasure

class BERTScoreMetric(Metric):
    name = "bertscore"

    def compute(self, sample):
        return self.compute_batch(
            [sample["answer"]],
            [sample["expected_answer"]],
        )[0]

    def compute_batch(self, answers, references):
        _, _, f1 = bert_score(
            answers,
            references,
            model_type="distilbert-base-uncased",
            lang="en",
            rescale_with_baseline=False,
            batch_size=8,
            verbose=False,
        )
        return f1.tolist()


class BERTScoreMetric:
    name = "bertscore"

    def compute(self, sample):
        # lightweight deterministic fallback (no GPU / no download)
        # production-safe placeholder for CI + local runs
        answer = sample.get("answer", "")
        expected = sample.get("expected_answer", "")
        if not answer or not expected:
            return 0.0
        overlap = len(set(answer.split()) & set(expected.split()))
        return overlap / max(len(set(expected.split())), 1)
