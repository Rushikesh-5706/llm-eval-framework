import os
from openai import OpenAI
from anthropic import Anthropic

def create_judge_client(provider: str):
    if provider == "openai":
        return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    if provider == "anthropic":
        return Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    raise ValueError(f"Unsupported judge provider: {provider}")
