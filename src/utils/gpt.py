import json
import openai
import traceback

from pydantic import BaseModel
from termcolor import colored
from typing import Any, Literal, Optional

from src.models.exceptions import AppError
from src.utils.llm import safe_message


ANSWER_TOOL = {
    "type": "function",
    "function": {
        "name": "respond",
        "description": "Send a message to the user.",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The message in Markdown.",
                },
            },
            "required": ["content"],
        },
    },
}
THINK_TOOL = {
    "type": "function",
    "function": {
        "name": "think",
        "description": "Think step by step before answering or invoking tools.",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": (
                        "Your personal thoughts, in Markdown. "
                        "The user never sees this."
                    ),
                },
            },
            "required": ["content"],
        },
    },
}


class ToolCall(BaseModel):
    id: str
    name: str
    arguments: dict[str, Any]


class Completion(BaseModel):
    answer: Optional[str]
    thinking: Optional[str]
    tool_calls: list[ToolCall]


def get_completion(
    messages: list[dict[str, Any]],
    max_tokens: int = 1000,
    model: Literal["gpt-4o"] = "gpt-4o",
    temperature: float = 0.0,
    tools: list[dict[str, Any]] = [],  # Tool.as_gpt() output
    force_final_answer: bool = False,
) -> Completion:
    try:
        completion = openai.ChatCompletion.create(
            max_tokens=max_tokens,
            messages=messages,
            model=model,
            temperature=temperature,
            tool_choice="none" if force_final_answer else "auto",
            tools=[ANSWER_TOOL, THINK_TOOL, *tools] if tools else None,
        )  # type: ignore

        answer: str = ""
        thinking: str = ""
        tool_calls: list[ToolCall] = []

        response = completion.choices[0].message  # type: ignore

        if hasattr(response, "content") and response.content:
            chunk_content: str = response.content + "\n\n"
            answer = chunk_content
            print(colored(f"Answer: {chunk_content}", "blue"), end="")

        if hasattr(response, "tool_calls") and response.tool_calls:
            for tool_call in response.tool_calls:
                arguments = json.loads(safe_message(tool_call.function.arguments))

                if tool_call.function.name == "respond":
                    chunk_content = arguments["content"] + "\n"
                    answer += chunk_content
                    print(colored(f"Answer: {chunk_content}", "blue"), end="")
                    continue

                if tool_call.function.name == "think":
                    chunk_content = arguments["content"] + "\n"
                    thinking += chunk_content
                    print(colored(f"Thought: {chunk_content}", "blue"), end="")
                    continue

                parsed = ToolCall(
                    id=tool_call.id,
                    name=tool_call.function.name,
                    arguments=arguments,
                )

                print(colored(f"Tool: {parsed.json()}", "blue"))
                tool_calls.append(parsed)

        return Completion(
            answer=safe_message(answer.strip()) if answer else None,
            thinking=safe_message(thinking.strip()) if thinking else None,
            tool_calls=tool_calls,
        )

    except Exception as e:
        print(colored(traceback.format_exc(), "red"))
        raise AppError(f"Malformed response from LLM: {e}") from e
