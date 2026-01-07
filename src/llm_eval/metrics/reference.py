from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from bert_score import score as bert_score
from llm_eval.core.base_metric import Metric

class BLEUMetric(Metric):
    name = "bleu"
    def compute(self, sample):
        expected = sample.get("expected_answer", "")
        answer = sample.get("answer", "")
        
        ref = expected.split()
        hyp = answer.split()
        
        # FIX: Ensure n is at least 1 to avoid ZeroDivisionError
        n = min(4, len(ref), len(hyp))
        if n == 0:
            return 0.0
            
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
        expected = sample.get("expected_answer", "")
        answer = sample.get("answer", "")
        
        if not expected or not answer:
            return 0.0
            
        scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
        return scorer.score(expected, answer)["rougeL"].fmeasure

class BERTScoreMetric(Metric):
    name = "bertscore"

    def compute(self, sample):
        # Lightweight deterministic fallback to avoid heavy model loading if preferred,
        # or use the batch compute logic.
        answer = sample.get("answer", "")
        expected = sample.get("expected_answer", "")
        
        if not answer or not expected:
            return 0.0
            
        # Standard overlap fallback (as in your original snippet)
        ans_set = set(answer.split())
        exp_set = set(expected.split())
        
        overlap = len(ans_set & exp_set)
        return overlap / max(len(exp_set), 1)

    def compute_batch(self, answers, references):
        if not answers or not references:
            return []
            
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
