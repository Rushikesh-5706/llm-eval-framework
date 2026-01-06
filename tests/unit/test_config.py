from llm_eval.config.schema import EvalConfig
from llm_eval.config.judge_schema import JudgeConfig, JudgeRubric

def test_eval_config_load():
    cfg = EvalConfig(
        dataset_path="d",
        output_dir="o",
        models={"m": "p"},
        metrics=["bleu"],
        judge=None
    )
    assert cfg.dataset_path == "d"

def test_judge_schema():
    rubric = JudgeRubric(
        coherence="c",
        relevance="r",
        safety="s"
    )
    cfg = JudgeConfig(
        provider="openai",
        model="gpt",
        rubric=rubric
    )
    assert cfg.provider == "openai"
