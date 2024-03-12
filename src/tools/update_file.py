from pydantic import BaseModel
from typing import Type

from src.models.state import State
from src.models.tool import Tool
from typing import Optional
import pathlib


class _Args(BaseModel):
    file_path: pathlib.Path
    new_content: Optional[str] = None


class UpdateFile(Tool):
    name: str = "update_file"
    description: str = "Updates the contents of a file."
    args_type: Type[_Args] = _Args

    def _run(self, state: State, args: _Args) -> str:
        file_path = args.file_path
        new_content = args.new_content

        # Check if the file exists
        if not file_path.exists():
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        # Read the current contents of the file
        with file_path.open("r") as file:
            current_content = file.read()

        # Update the contents of the file
        if new_content is not None:
            current_content = new_content

        # Write the updated contents back to the file
        with file_path.open("w") as file:
            file.write(current_content)

        return current_content
