import json
from tenacity import retry, wait_exponential, stop_after_attempt
from llm_eval.judge.prompt import build_judge_prompt

class LLMJudge:
    def __init__(self, client, config):
        self.client = client
        self.config = config

    @retry(wait=wait_exponential(min=1, max=10),
           stop=stop_after_attempt(3))
    def evaluate(self, query: str, answer: str) -> dict:
        prompt = build_judge_prompt(
            query=query,
            answer=answer,
            rubric=self.config.rubric.model_dump()
        )

        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.config.temperature,
        )

        content = response.choices[0].message.content
        return json.loads(content)
