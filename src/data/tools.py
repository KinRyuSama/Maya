from functools import cache

from src.models.tool import Tool
from src.tools.echo import Echo


@cache
def list_tools() -> list[Tool]:
    return [
        Echo(),
    ]
