"""Simple interface for interacting with multiple LLM providers."""

from typing import Optional, List, Dict
import os
import openai

PROVIDERS = {
    "openai": openai,
}


def query_llm(provider: str, prompt: str, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo") -> str:
    """Send a prompt to the selected LLM provider and return the response."""
    if provider not in PROVIDERS:
        raise ValueError(f"Unsupported provider: {provider}")
    if api_key:
        openai.api_key = api_key
    resp = openai.ChatCompletion.create(model=model, messages=[{"role": "user", "content": prompt}])
    return resp.choices[0].message["content"].strip()
