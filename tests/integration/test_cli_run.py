import subprocess
import sys
from pathlib import Path
import json

def test_cli_run(tmp_path):
    dataset = tmp_path / "d.jsonl"
    dataset.write_text(
        '{"query":"q","expected_answer":"a","retrieved_contexts":["a"]}\n'
    )

    outputs = tmp_path / "out.jsonl"
    outputs.write_text(
        '{"id": 0, "answer": "a"}\n'
    )

    cfg = tmp_path / "cfg.json"
    cfg.write_text(json.dumps({
        "dataset_path": str(dataset),
        "output_dir": str(tmp_path),
        "models": {"m": str(outputs)},
        "metrics": ["bleu"]
    }))

    result = subprocess.run(
        [sys.executable, "-m", "llm_eval.cli.main",
         "--config", str(cfg),
         "--output-dir", str(tmp_path)],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert (tmp_path / "results.json").exists()
