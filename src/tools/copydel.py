from pydantic import BaseModel
from typing import Literal, Type

from src.models.tool import Tool
from src.models.state import State

import os


class _Args(BaseModel):
    file_name: str
    action: Literal["create", "delete"]


class Copydel(Tool):
    name: str = "copydel"
    description: str = "create and delete files in folder"
    args_type: Type[BaseModel] = _Args

    def _run(self, state: State, args: _Args) -> str:
        if args.action == "create":
            self._create_file(args.file_name)
        elif args.action == "delete":
            self._delete_file(args.file_name)
        else:
            raise ValueError("Invalid action specified. Must be 'create' or 'delete'.")
        return f"Successfully {args.action}ed file {args.file_name}"

    def _create_file(self, file_name: str):
        file_name = "test 2"

        if not os.path.exists(file_name):
            # os.makedirs(file_name)
            pass  # TODO DELETE THE FILE
        else:
            raise FileExistsError(f"File {file_name} already exists.")

    def _delete_file(self, file_name: str):
        if os.path.exists(file_name):
            # os.rmdir(file_name)
            pass  # TODO DELETE THE FILE
        else:
            raise FileNotFoundError(f"File {file_name} not found.")
