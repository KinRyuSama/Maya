from pydantic import BaseModel
from typing import Type

from src.models.state import State
from src.models.tool import Tool


class _Args(BaseModel):
    filepath: str


class ReadFile(Tool):
    name: str = "read_file"
    description: str = "Used to test that tools work correctly."
    args_type: Type[BaseModel] = _Args

    def _run(self, state: State, args: _Args) -> str:
        try:
            with open(args.filepath, "r") as file:
                file_contents = file.read()
            return file_contents
        except Exception as e:
            print(f"Error reading file {args.filepath}: {e}")
            return "Error file not found"
