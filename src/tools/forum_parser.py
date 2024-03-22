import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import Type

from src.models.state import State
from src.models.tool import Tool


class _Args(BaseModel):
    url: str


class ForumParser(Tool):
    name: str = "forum_parser"
    description: str = "Used to parse HTML content and extract information."
    args_type: Type[_Args] = _Args

    def _run(self, state: State, args: _Args):
        response = requests.get(args.url)
        return _parse_forum(response.text)


def _parse_forum(html: str):
    page = BeautifulSoup(html, "html.parser")
    posts = page.select("td.row1, td.row2")  # select the posts from forum

    for post in posts:
        pub = post.select_one("span.postdetails")
        if pub and "Publicité" in pub.text:
            continue
        post_body = post.select_one("span.postbody")
        if post_body:
            return post_body.text
