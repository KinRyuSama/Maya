from pydantic import BaseModel
from typing import Type
import os

from src.models.state import State
from src.models.tool import Tool

IGNORED = [
    ".git/",
    ".vscode/",
    "__pycache__/",
    ".venv/",
    "src/",
    "README.md",
    ".gitignore",
    ".pytest_cache/",
    "requirements.txt",
    ".gitignore",
    ".env",
]


class _Args(BaseModel):
    pass


class ListFiles(Tool):
    name: str = "list_files"
    description: str = "Used to test that tools work correctly."
    args_type: Type[BaseModel] = _Args

    def _run(self, state: State, args: _Args) -> str:
        directory = (
            "/home/nate/Desktop/Maya"  # Ensure this path is correct and case-sensitive
        )
        all_files = []  # Initialize the list to store file paths

        try:
            for root, _, files in os.walk(directory):
                for file in files:
                    absolute_path = os.path.join(root, file)
                    relative_path = os.path.relpath(absolute_path, directory)
                    # if relative_path contains anything from IGNORED, skipnit!
                    if any(pattern in relative_path for pattern in IGNORED):
                        continue
                    else:
                        all_files.append(relative_path)
            return "\n".join(
                all_files
            )  # Return the list of files as a newline-separated string
        except Exception as exc:
            return str(exc)  # Return the error message if any
