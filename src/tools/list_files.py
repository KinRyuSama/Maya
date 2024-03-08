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
        directory = "/home/nathan/Desktop/Maya"  # Ensure this path is correct and case-sensitive
        all_files = []  # Initialize the list to store file paths

        try:
            for root, _, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(
                        root, file
                    )  # Combine directory and file name
                    all_files.append(file_path)  # Add the file path to the list
            return "\n".join(
                all_files
            )  # Return the list of files as a newline-separated string
        except Exception as exc:
            return str(exc)  # Return the error message if any
