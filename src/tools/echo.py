from pydantic import BaseModel
from typing import Type

from src.models.state import State
from src.models.tool import Tool


class _Args(BaseModel):
    text: str


class Echo(Tool):
    name: str = "echo"
    description: str = "Used to test that tools work correctly."
    args_type: Type[BaseModel] = _Args

    def _run(self, state: State, args: _Args) -> str:
        # raise AppError("dummy error")  # testing errors
        return args.text  # testing success
