import json

from dataclasses import dataclass
from pydantic import BaseModel
from termcolor import colored
from typing import Any, Optional

from src.data.tools import list_tools
from src.models.state import State
from src.models.tool import ToolResult
from src.utils.gpt import get_completion, ToolCall
from src.utils.llm import get_num_gpt_tokens_messages, get_num_tokens


MAX_STEPS = 3  # account for 'thinking' tool

LAST_STEP_PROMPT = f"""
Observation: \
You have exhausted the limit of {MAX_STEPS} reasoning steps. \
Please generate a final response from what you have gathered.
""".strip()


class AgentResult(BaseModel):
    content: str


@dataclass
class StepOutput:
    answer: Optional[str]
    """
    The final answer generated by the LLM.
    Corresponds to the "final_answer" tool or an absence of tool calls.
    Also filled when a tool uses 'delegate: true'.
    """
    thinking: Optional[str]
    """
    Thinking that occurred before the agent invoked "real tools".
    Corresponds to the "thinking" tool in `get_openai_completion_with_tools`.
    """
    tools: list[tuple[ToolCall, ToolResult]]
    """
    The tools that were invoked in that step, along with their outcome.
    """


@dataclass
class ChatAgent:
    def on_message(self, state: State, prompt: str) -> AgentResult:
        if len(state.history) == 0:
            print(colored("---\nTools:", "yellow"))
            print(
                colored(
                    "\n".join([json.dumps(t.as_gpt(), indent=2) for t in list_tools()]),
                    "yellow",
                )
            )
            print(colored("---", "yellow"))

        print(colored(self._system_prompt(), "yellow"))

        prompt_message = {"role": "user", "content": prompt}
        new_history = [prompt_message]
        memory = [*state.history, prompt_message]
        final_answer: Optional[str] = None

        for index in range(MAX_STEPS + 1):
            step_output: StepOutput = self._step(
                state=state,
                memory=memory,
                force_final_answer=index == MAX_STEPS,
            )

            # In the history, batch tool calls before tool results
            # Add to memory (which is constrained) AND history (which isn't)
            if step_output.thinking:
                message = {"role": "assistant", "content": step_output.thinking}
                new_history.append(message)
                memory.append(message)

            # Add tool calls to the history
            if step_output.tools:
                tool_calls = []
                for tool_call, _ in step_output.tools:
                    tool_calls.append(
                        {
                            "type": "function",
                            "id": tool_call.id,
                            "function": {
                                "name": tool_call.name,
                                "arguments": json.dumps(tool_call.arguments),
                            },
                        }
                    )

                tool_call_message = {
                    "role": "assistant",
                    "tool_calls": tool_calls,
                }
                new_history.append(tool_call_message)
                memory.append(tool_call_message)

                for tool_call, tool_result in step_output.tools:
                    tool_result_message = {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_call.name,
                        "content": tool_result.json(),
                    }
                    new_history.append(tool_result_message)
                    memory.append(tool_result_message)

            # Return the final answer if present
            if step_output.answer:
                final_answer = step_output.answer
                break

        # The last step always contains a final_answer
        assert final_answer

        # Only persist this interaction in the history if it was successful, so
        # the agent does not get stuck in a corrupted state
        state.extend_history(
            [*new_history, {"role": "assistant", "content": final_answer}]
        )

        return AgentResult(content=final_answer)

    def _system_prompt(self) -> str:
        return """
You are a useful assistant.
""".strip()

    def _step(
        self,
        state: State,
        force_final_answer: bool,
        memory: list[dict[str, Any]],
    ) -> StepOutput:
        system = self._system_prompt()
        tools = list_tools()
        gpt_tools = [t.as_gpt() for t in tools]

        # Request that the model generate the final answer, but do not include
        # in conversation history.
        if force_final_answer:
            memory = [*memory, {"role": "user", "content": LAST_STEP_PROMPT}]

        # Pick as many messages as fit in the LLM token limit
        _constrain_memory(memory, system, gpt_tools)

        completion = get_completion(
            messages=[{"role": "system", "content": system}, *memory],
            max_tokens=4096,
            model="gpt-4o",
            temperature=0.4,
            tools=gpt_tools,
            force_final_answer=force_final_answer,
        )

        # If the LLM returned a final answer, do not call tools.
        if completion.answer:
            return StepOutput(
                answer=completion.answer,
                thinking=completion.thinking,
                tools=[],
            )

        # Call the tools and gather their outputs
        tool_results: list[tuple[ToolCall, ToolResult]] = []
        for tool_call in completion.tool_calls:
            tool = next(tool for tool in tools if tool.name == tool_call.name)
            result = tool.run(state, tool_call.arguments)
            tool_results.append((tool_call, result))

        # The observations become the input of the next reasoning step
        return StepOutput(
            answer=completion.answer,
            thinking=completion.thinking,
            tools=tool_results,
        )


def _constrain_memory(
    memory: list[dict[str, Any]],
    system: str,
    gpt_tools: list[dict[str, Any]],
) -> None:
    MEMORY_TOKEN_LIMIT = 7000  # 7h input + 1k output = 8k total tokens
    system_tokens = get_num_tokens("gpt-4", system, True, gpt_tools)

    # Pop the earliest message first
    memory.reverse()

    # Pop interactions until they fit
    while system_tokens + get_num_gpt_tokens_messages(memory) > MEMORY_TOKEN_LIMIT:
        memory.pop()
        while memory and memory[-1]["role"] != "user":
            memory.pop()

    # Render the conversation in chronological order
    memory.reverse()
