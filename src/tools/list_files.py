from pydantic import BaseModel
from typing import Type
import os

from src.models.state import State
from src.models.tool import Tool


class _Args(BaseModel):
    text: str


class ListFiles(Tool):
    name: str = "list_files"
    description: str = "Used to test that tools work correctly."
    args_type: Type[BaseModel] = _Args

    def _run(self, state: State, args: _Args) -> str:
        directory = "/Home/Desktop/Maya"
        try:
            os.listdir(directory)
            return "\n".join(ListFiles)
        except Exception as _args:
            return str(_Args)
