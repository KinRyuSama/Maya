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
        print(colored(result.content, "magenta"))


if __name__ == "__main__":
    while True:
        prompt = input(" To Maya >> ")
        run(prompt)
