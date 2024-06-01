from pydantic import BaseModel
from typing import Literal, Type

from src.models.tool import Tool
from src.models.state import State

import os


class _Args(BaseModel):
    file_name: str
<<<<<<< HEAD
    action: Literal["delete"]


class DeleteFile(Tool):
    name: str = "Delete_File"
    description: str = "delete files in folder"
=======
    action: Literal["create"]


<<<<<<<< HEAD:src/tools/createfile.py
class CreateFile(Tool):
    name: str = "create_file"
    description: str = "create files in folder"
    args_type: Type[BaseModel] = _Args

    def _run(self, state: State, args: _Args) -> str:
        if args.action == "create":
            self._create_file(args.file_name)
========
class Delete_File(Tool):
    name: str = "Delete File"
    description: str = "Create and Delete files in folder"
>>>>>>> 3e6247317d623e10e3f13e9c6b77b3cd66ecd036
    args_type: Type[BaseModel] = _Args

    def _run(self, state: State, args: _Args) -> str:
        if args.action == "delete":
            self._delete_file(args.file_name)
<<<<<<< HEAD
        else:
            raise ValueError("Invalid action specified. Must be 'create' or 'delete'.")
        return f"Successfully {args.action}ed file {args.file_name}"

=======
>>>>>>>> 3e6247317d623e10e3f13e9c6b77b3cd66ecd036:src/tools/deletefile.py
        else:
            raise ValueError("Invalid action specified. Must be 'create'.")
        return f"Successfully {args.action}ed file {args.file_name}"

<<<<<<<< HEAD:src/tools/createfile.py
    def _create_file(self, file_name: str):
        if not os.path.exists(file_name):
            # os.makedirs(file_name)
            open(file_name, "w").close()
        else:
            raise FileExistsError(f"File {file_name} already exists.")
========
>>>>>>> 3e6247317d623e10e3f13e9c6b77b3cd66ecd036
    def _delete_file(self, file_name: str):
        if os.path.exists(file_name):
            # os.rmdir(file_name)
            os.remove(file_name)
        else:
            raise FileNotFoundError(f"File {file_name} not found.")
<<<<<<< HEAD
=======
>>>>>>>> 3e6247317d623e10e3f13e9c6b77b3cd66ecd036:src/tools/deletefile.py
>>>>>>> 3e6247317d623e10e3f13e9c6b77b3cd66ecd036
