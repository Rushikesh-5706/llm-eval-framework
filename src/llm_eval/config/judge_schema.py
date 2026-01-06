from pydantic import BaseModel, Field
from typing import List

class JudgeRubric(BaseModel):
    coherence: str = Field(..., description="Logical consistency and clarity")
    relevance: str = Field(..., description="Answer relevance to query")
    safety: str = Field(..., description="No harmful or unsafe content")

class JudgeConfig(BaseModel):
    provider: str
    model: str
    temperature: float = 0.0
    max_retries: int = 3
    rubric: JudgeRubric
