from typing import Dict, List, Optional
from pydantic import BaseModel
from llm_eval.config.judge_schema import JudgeConfig


class EvalConfig(BaseModel):
    dataset_path: str
    models: Dict[str, str]
    metrics: List[str]
    judge: Optional[JudgeConfig] = None

