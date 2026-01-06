import pandas as pd
from llm_eval.reporting.aggregate import aggregate
from llm_eval.reporting.writers import write_json, write_markdown

def test_reporting(tmp_path):
    results = [
        {"model": "m", "query": "q", "scores": {"bleu": 0.5}}
    ]
    df, stats = aggregate(results)
    assert not df.empty
    assert not stats.empty

    write_json(tmp_path / "r.json", results)
    write_markdown(tmp_path / "r.md", stats)

