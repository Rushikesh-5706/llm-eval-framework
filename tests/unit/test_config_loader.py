import json
from llm_eval.config.loader import load_config

def test_json_loader(tmp_path):
    cfg = {
        "dataset_path": "d",
        "output_dir": "o",
        "models": {"m": "p"},
        "metrics": ["bleu"]
    }
    p = tmp_path / "c.json"
    p.write_text(json.dumps(cfg))
    loaded = load_config(str(p))
    assert loaded.dataset_path == "d"
