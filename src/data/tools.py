from functools import cache

from src.models.tool import Tool
from src.tools.echo import Echo
from src.tools.create_delete import Create_Delete
from src.tools.list_files import ListFiles
from src.tools.manage_folders import ManageFolders
from src.tools.read_file import ReadFile
from src.tools.update_file import UpdateFile
from src.tools.parser import Parser


@cache
def list_tools() -> list[Tool]:
    return [
        Echo(),
        Create_Delete(),
        ListFiles(),
        ManageFolders(),
        ReadFile(),
        UpdateFile(),
        Parser(),
    ]
