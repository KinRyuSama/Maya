import requests
import html2text
from pydantic import BaseModel
from typing import Type
from src.models.tool import Tool
from abc import ABC, abstractmethod


class Request(ABC):
    name: str
    description: str

    @abstractmethod
    def run(self, *args, **kwargs):
        pass


class _Args(BaseModel):
    url: str


class RequestUrl(Tool):
    name: str = "request_url"
    description: str = "Used to test that tools work correctly."
    args_type: Type[_Args] = _Args

    def run(self, args: _Args) -> str:
        response = requests.get(args.url)
        response.raise_for_status()  # Ensure the request was successful

        # Convert the response text to Markdown format if necessary
        if response.headers.get("Content-Type", "").startswith("text/html"):
            html2text_converter = html2text.HTML2Text()
            response = html2text_converter.handle(response.text)
        else:
            response = response.text

        return response


# Get the URL from the user
url = input("Enter the URL you want to request: ")

# Create an instance of the RequestUrl class
request_tool = RequestUrl()

# Call the run method to make the request and read the content
content = request_tool.run(_Args(url=url))

# Print the content
print(content)
