# flake8: noqa
from dataclasses import dataclass
from typing import Optional

BASE_URL = "https://openrouter.ai/api/v1/chat/completions"


@dataclass
class OpenRouterHeaders:
    api_key: str
    content_type: str = "application/json"

    @property
    def as_dict(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": self.content_type,
        }


@dataclass
class ModelConfig:
    model_name: str
    max_tokens: int = 2000
    temperature: float = 0.1
    system_prompt: Optional[str] = None


DEFAULT_MODEL = ModelConfig(
    model_name="google/gemini-2.0-flash-001",
    max_tokens=2000,
    temperature=0.1,
    system_prompt="You are a helpful assistant that summarizes gene-disease associations.",
)

MODEL_WITH_FORMAT = ModelConfig(
    model_name="google/gemini-2.0-flash-001",
    max_tokens=2000,
    temperature=0.1,
    system_prompt=(
        "You are a helpful assistant that summarizes gene-disease associations. "
        "You must strictly respond in the following JSON format:\n"
        "{\n"
        '  "summary_text": str,\n'
        '  "key_findings": [str],\n'
        '  "confidence": float (0.0 - 1.0, optional)\n'
        "}\n"
        "Do not include any extra text outside this JSON. "
        "If any field is missing or unknown, use empty string or empty array or null."
    ),
)
