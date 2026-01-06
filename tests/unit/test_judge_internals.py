import os
import pytest
from llm_eval.judge.prompt import build_judge_prompt
from llm_eval.judge.client import create_judge_client

def test_prompt_build():
    p = build_judge_prompt(
        query="q",
        answer="a",
        rubric={"coherence": "c", "relevance": "r", "safety": "s"}
    )
    assert "QUERY" in p
    assert "ANSWER" in p

def test_invalid_provider():
    with pytest.raises(ValueError):
        create_judge_client("invalid")

