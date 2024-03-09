from pydantic import BaseModel
from typing import Type

from src.models.state import State
from src.models.tool import Tool


class _Args(BaseModel):
    text: str
    file_path: str


class ReadFile(Tool):
    name: str = "read_file"
    description: str = "Used to test that tools work correctly."
    args_type: Type[BaseModel] = _Args

    def _run(self, state: State, args: _Args) -> str:
        try:
            with open(args.file_path, "r") as file:
                file_contents = file.read()
            return file_contents
        except Exception as e:
            print(f"Error reading file {args.file_path}: {e}")
            return None
