"""Permit Setu: Azure OpenAI client wrapper.

Provides text-chat AND vision-chat completion helpers for Permit Setu agents.

NOTE on reasoning models (gpt-5.x, o1, o3): the OpenAI API renamed `max_tokens`
to `max_completion_tokens` for these models, and some reject custom
`temperature` values. This wrapper uses `max_completion_tokens` exclusively and
treats `temperature` as optional — pass None (the default) to omit it from the
request, which works for ALL deployments.
"""
from typing import List, Dict, Any, Optional
from openai import AzureOpenAI, BadRequestError

from app.config import settings


def get_client() -> AzureOpenAI:
    """Construct an AzureOpenAI client from settings."""
    settings.validate()
    return AzureOpenAI(
        api_key=settings.AZURE_OPENAI_API_KEY,
        api_version=settings.AZURE_OPENAI_API_VERSION,
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
    )


def _drop_unsupported(kwargs: Dict[str, Any], err_msg: str) -> Dict[str, Any]:
    """Best-effort retry helper.

    When the API returns an `unsupported_parameter` error naming a specific
    parameter, strip that parameter from kwargs and retry once. Handles
    `temperature`, `top_p`, `response_format`, and others that some reasoning
    models reject.
    """
    err = err_msg.lower()
    for p in ["temperature", "top_p", "presence_penalty", "frequency_penalty",
              "response_format", "max_tokens"]:
        if f"'{p}'" in err or f'"{p}"' in err or f" {p} " in err:
            if p in kwargs:
                kwargs.pop(p)
                return kwargs
    return kwargs


def _create_with_retry(client: AzureOpenAI, kwargs: Dict[str, Any]) -> Any:
    """Call create() and retry once if a parameter isn't supported."""
    try:
        return client.chat.completions.create(**kwargs)
    except BadRequestError as e:
        msg = str(e)
        if "unsupported_parameter" in msg.lower() or "unsupported parameter" in msg.lower():
            new_kwargs = _drop_unsupported(dict(kwargs), msg)
            if new_kwargs != kwargs:
                # Retry once
                return client.chat.completions.create(**new_kwargs)
        raise


# ============================================================
# Text-only chat
# ============================================================

def call_chat(
    messages: List[Dict[str, Any]],
    temperature: Optional[float] = None,
    max_completion_tokens: int = 4000,
    response_format: Optional[Dict[str, str]] = None,
    deployment: Optional[str] = None,
) -> str:
    """Run a chat completion against the configured Azure OpenAI deployment.

    Args:
        messages: OpenAI-format messages.
        temperature: Sampling temperature (0.0-1.0) — OMITTED from request if None.
            Reasoning models (gpt-5.x, o1, o3) reject custom temperature values,
            so pass None (the default) to be compatible with both reasoning and
            non-reasoning deployments.
        max_completion_tokens: Maximum completion tokens. (Replaces the legacy
            `max_tokens` parameter, which gpt-5.x rejects.)
        response_format: Optional {"type": "json_object"} for JSON-mode.
        deployment: Optional deployment name override.

    Returns:
        The completion content as a string.
    """
    client = get_client()
    kwargs: Dict[str, Any] = {
        "model": deployment or settings.AZURE_OPENAI_DEPLOYMENT_NAME,
        "messages": messages,
        "max_completion_tokens": max_completion_tokens,
    }
    if temperature is not None:
        kwargs["temperature"] = temperature
    if response_format is not None:
        kwargs["response_format"] = response_format

    response = _create_with_retry(client, kwargs)
    return response.choices[0].message.content or ""


def call_chat_json(
    messages: List[Dict[str, Any]],
    temperature: Optional[float] = None,
    max_completion_tokens: int = 4000,
) -> str:
    """Convenience wrapper that forces JSON-mode responses."""
    return call_chat(
        messages=messages,
        temperature=temperature,
        max_completion_tokens=max_completion_tokens,
        response_format={"type": "json_object"},
    )


# ============================================================
# Vision chat — multimodal input (text + images)
# ============================================================

def call_vision(
    system_prompt: str,
    user_text: str,
    image_data_urls: List[str],
    temperature: Optional[float] = None,
    max_completion_tokens: int = 4000,
    detail: str = "auto",
    response_format: Optional[Dict[str, str]] = None,
    deployment: Optional[str] = None,
) -> str:
    """Run a multimodal (text + image) chat completion.

    Args:
        system_prompt: System instruction text.
        user_text: User textual question/task.
        image_data_urls: List of base64 data URLs or http(s) image URLs.
        temperature: Sampling temperature — OMITTED if None (default).
        max_completion_tokens: Max completion tokens.
        detail: "auto" | "low" | "high".
        response_format: Optional JSON-mode flag.
        deployment: Optional deployment override.

    Returns:
        The completion content as a string.
    """
    client = get_client()

    user_content: List[Dict[str, Any]] = [{"type": "text", "text": user_text}]
    for url in image_data_urls:
        user_content.append(
            {
                "type": "image_url",
                "image_url": {"url": url, "detail": detail},
            }
        )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]

    vision_deployment = (
        deployment
        or settings.AZURE_OPENAI_VISION_DEPLOYMENT_NAME
        or settings.AZURE_OPENAI_DEPLOYMENT_NAME
    )

    kwargs: Dict[str, Any] = {
        "model": vision_deployment,
        "messages": messages,
        "max_completion_tokens": max_completion_tokens,
    }
    if temperature is not None:
        kwargs["temperature"] = temperature
    if response_format is not None:
        kwargs["response_format"] = response_format

    response = _create_with_retry(client, kwargs)
    return response.choices[0].message.content or ""
