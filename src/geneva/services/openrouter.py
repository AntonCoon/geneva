import json
from typing import Any, Dict, Optional

import httpx

from .base import LLMService
from .openrouter_config import BASE_URL, MODEL_WITH_FORMAT, OpenRouterHeaders


class OpenRouterService(LLMService):
    def __init__(self, api_key: str, model_config=MODEL_WITH_FORMAT):
        self.headers = OpenRouterHeaders(api_key=api_key).as_dict
        self.model_config = model_config
        self.base_url = BASE_URL
        self.model_name = model_config.model_name

    def _ask_model(self, prompt: str) -> str:
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": self.model_config.max_tokens,
            "temperature": self.model_config.temperature,
        }

        try:
            with httpx.Client(timeout=30) as client:
                response = client.post(
                    self.base_url, headers=self.headers, json=payload
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"Error: {str(e)}"

    def summarize_gene_disease(
        self, data: Dict[str, Any], additional_context: Optional[str] = None
    ) -> Dict[str, Any]:
        gene = data.get("gene", "Unknown")
        disease = data.get("disease", "Unknown")

        prompt = (
            f"{self.model_config.system_prompt}\n\n"
            f"Gene: {gene}\n"
            f"Disease: {disease}\n"
            f"Data: {json.dumps(data, indent=2)}"
        )

        if additional_context:
            prompt += f"\n\nContext: {additional_context}"

        response_text = self._ask_model(prompt)

        try:
            if response_text.startswith("```"):
                response_text = "\n".join(response_text.splitlines()[1:-1])

            summary_json = json.loads(response_text)

            summary_json.setdefault("summary_text", "")
            summary_json.setdefault("key_findings", [])
            summary_json.setdefault("confidence", None)

        except json.JSONDecodeError:
            summary_json = {
                "summary_text": response_text,
                "key_findings": [],
                "confidence": None,
            }

        return summary_json
