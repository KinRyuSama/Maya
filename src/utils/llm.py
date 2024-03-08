import json
import tiktoken

from termcolor import colored
from typing import Any, Optional

TOKENS_PER_IMAGE_TILE = 170  # one tile is 512 x 512 pixels
ESTIMATED_TOKENS_PER_IMAGE = 170 * 4  # assuming average of 1024 x 1024
BUFFER_TOOL_DEFINITION = 20  # estimated tokens for OpenAI formatting
BUFFER_TOOL_CALL = 10  # estimated tokens for OpenAI formatting


def get_num_tokens(
    model: str,
    prompt: str | list[dict[str, str]],
    add_seps: bool = False,
    openai_tools: Optional[list[dict[str, Any]]] = None,
) -> int:
    """
    Return the number of tokens in the prompt.
    Supports images, although those tokens are only estimates.
    If `add_seps` is True, count "<|startoftext|>{role}:" and "<|endoftext|>".
    """
    if model.startswith("gpt-3.5"):
        model = "gpt-3.5-turbo-0301"
    elif model.startswith("gpt-4"):
        model = "gpt-4-0314"

    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print(
            colored(
                f"Warning: encoding for model {model} not found. Using cl100k_base.",
                "yellow",
            )
        )
        encoding = tiktoken.get_encoding("cl100k_base")

    if isinstance(prompt, str):
        prompt_tokens = len(encoding.encode(prompt, disallowed_special=()))
    elif isinstance(prompt, list):
        prompt_tokens = 0
        for part in prompt:
            if part["type"] == "image_url":
                prompt_tokens += ESTIMATED_TOKENS_PER_IMAGE
            elif part["type"] == "text":
                prompt_tokens += get_num_tokens(model, part["text"], False)

    if add_seps:
        prompt_tokens += 4

    if openai_tools:
        tools_json = json.dumps(openai_tools)
        tools_tokens = len(encoding.encode(tools_json, disallowed_special=()))
        prompt_tokens += tools_tokens + BUFFER_TOOL_DEFINITION

    return prompt_tokens


def get_num_gpt_tokens_messages(
    messages: list[dict[str, Any]],
    openai_tools: Optional[list[dict[str, Any]]] = None,
) -> int:
    """
    Estimate how many tokens the request takes.
    Format: sum("<start>role:content<end>" for messages) + "<start>assistant:"
    """
    total_tokens = 0

    for message in messages:
        if message["role"] == "system" and openai_tools:
            total_tokens += get_num_tokens("gpt-4", "", False, openai_tools)
        if content := message.get("content"):
            total_tokens += get_num_tokens("gpt-4", content, True)
        if message["role"] == "tool":
            total_tokens += get_num_tokens("gpt-4", message["tool_call_id"], False)
            total_tokens += get_num_tokens("gpt-4", message["tool_call_id"], False)
            total_tokens += BUFFER_TOOL_CALL
        if message.get("tool_calls"):
            tool_calls_json = json.dumps(message["tool_calls"])
            total_tokens += get_num_tokens("gpt-4", tool_calls_json, False)
            total_tokens += BUFFER_TOOL_CALL

    return total_tokens + 3


def safe_message(content: str) -> str:
    """
    Langchain does not expose tiktoken params to allow special tokens.
    So we "escape" them to prevent an exception.
    Side effect: messages are not exactly the same as the original.
    """
    return content.replace("<|endoftext|>", "<||endoftext||>")


def strip_ticks(completion: str, ticks: str = "```") -> str:
    """
    If you want the AI to wrap something in a block, between separators, this
    allows you to extract the content of that block, ignoring anything outside.
    It allows the AI to think before giving you its answer.
    """
    try:
        code_start = completion.index(ticks)
        lines = completion[code_start:].splitlines()[1:]
        position = lines.index(ticks)
        return "\n".join(lines[:position])
    except ValueError:
        pass  # no ticks found, therefore, keep the response as-is

    return completion
