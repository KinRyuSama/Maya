from pydantic import BaseModel
from typing import Type, Literal

from src.models.state import State
from src.models.tool import Tool

import os


class _Args(BaseModel):
    text: str
    action: Literal["create"]  # added action attribute


class CreateFolder(Tool):
    name: str = "create_folder"
    description: str = "Used to create folders."
    args_type: Type[_Args] = _Args

    def _run(self, state: State, args: _Args) -> str:
        if args.action == "create":
            self._create_folder(args.text)
        else:
            raise ValueError("Invalid action specified. Must be 'create'.")
        return f"Successfully {args.action}ed folder {args.text}"

    def _create_folder(self, folder_name: str):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        else:
            raise FileExistsError(f"Folder {folder_name} already exists.")
