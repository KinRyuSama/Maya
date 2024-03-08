from pydantic import BaseModel
from typing import Any


class State(BaseModel):
    history: list[dict[str, Any]]

    @staticmethod
    def new() -> "State":
        return State(history=[])

    def extend_history(self, messages: list[dict[str, Any]]) -> None:
        self.history.extend(messages)
