import json
import yaml
from pathlib import Path
from llm_eval.config.schema import EvalConfig

def load_config(path: str) -> EvalConfig:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config not found: {path}")

    if p.suffix in {".yaml", ".yml"}:
        data = yaml.safe_load(p.read_text())
    elif p.suffix == ".json":
        data = json.loads(p.read_text())
    else:
        raise ValueError("Config must be YAML or JSON")

    return EvalConfig(**data)
