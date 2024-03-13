import json
import traceback

from pydantic import BaseModel, parse_obj_as
from termcolor import colored
from typing import Any, Optional, Type

from src.models.state import State


class ToolResult(BaseModel):
    answer: Optional[str] = None
    error: Optional[str] = None


class Tool(BaseModel):
    name: str
    """The unique name of the tool seen by the LLM."""
    description: str
    """Tells the LLM how/when/why to use the tool."""
    args_type: Type[BaseModel]
    """
    The type of the arguments sent to the tool by the LLM.
    Use this as the type of `args` in the `_run` method.
    """

    def as_gpt(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": self.schema(),
        }

    def schema(self) -> dict[str, Any]:
        """The schema sent to the LLM to teach it how to use the tool."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.args_type.schema(),
        }

    def run(self, state: State, input: dict[str, Any]) -> ToolResult:
        try:
            print(colored(f"CALL {self.name} ON {json.dumps(input)}", "yellow"))
            tool_input = parse_obj_as(self.args_type, input)
            answer = self._run(state, tool_input)
            print(colored(f'  -> """\n{answer}\n"""', "yellow"))
            return ToolResult(answer=answer)
        except Exception as e:
            print(colored(traceback.format_exc(), "red"))
            return ToolResult(error=str(e))

    def _run(self, state: State, args: Any) -> str:
        # Tip: replace `args: Any` by `args: _Args`
        raise NotImplementedError("Tool#_run must be implemented by subclass.")
