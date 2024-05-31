from functools import cache

from src.models.tool import Tool
from src.tools.echo import Echo
from tools.deletefile import Delete_File
from src.tools.list_files import ListFiles
from src.tools.manage_folders import ManageFolders
from src.tools.read_file import ReadFile
from src.tools.update_file import UpdateFile
from src.tools.parser import Parser
from src.tools.makefile import Create_File


@cache
def list_tools() -> list[Tool]:
    return [
        Echo(),
        ListFiles(),
        ManageFolders(),
        ReadFile(),
        UpdateFile(),
        Parser(),
        Create_File(),
        Delete_File(),
    ]
