from functools import cache

from src.models.tool import Tool
from src.tools.echo import Echo
from src.tools.createfile import CreateFile
from src.tools.deletefile import DeleteFile
from src.tools.list_files import ListFiles
from src.tools.read_file import ReadFile
from src.tools.update_file import UpdateFile
from src.tools.parser import Parser
from src.tools.createfolder import CreateFolder
from src.tools.deletefolder import DeleteFolder


@cache
def list_tools() -> list[Tool]:
    return [
        Echo(),
        ListFiles(),
        ReadFile(),
        UpdateFile(),
        Parser(),
        CreateFile(),
        DeleteFile(),
        CreateFolder(),
        DeleteFolder(),
    ]
