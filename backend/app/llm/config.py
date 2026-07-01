from dataclasses import dataclass


@dataclass
class LLMConfig:

    provider: str = "groq"

    model: str = "llama-3.3-70b-versatile"

    temperature: float = 0.2

    max_tokens: int = 4000

    stream: bool = True

    api_key: str | None = None

    base_url: str | None = None
