import sys

from termcolor import colored

from src.config import AppConfig  # noqa: F401
from src.agents.chat import ChatAgent
from src.models.state import State

state = State.new()


def run(prompt: str):
    global state
    prompt = prompt.strip()

    if prompt in ["exit", "/exit"]:
        sys.exit(0)

    else:
        result = ChatAgent().on_message(state, prompt)
        print(colored(result.content, "green"))


if __name__ == "__main__":
    while True:
        prompt = input(" RE4P3R > ")
        run(prompt)
