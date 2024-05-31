from pydantic import BaseModel
from typing import Type
import os
import requests
from bs4 import BeautifulSoup
import pdfplumber
from src.models.tool import Tool


class _Args(BaseModel):
    text: str


class Parser(Tool):
    name: str = "Parser"
    description: str = "Parse"
    args_type: Type[BaseModel] = _Args


def parse_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    divs = soup.find_all("div")  # Find all div tags
    div_texts = [
        div.get_text(separator=" ", strip=True) for div in divs
    ]  # Extract text from each div
    return "\n".join(div_texts)


def parse_folder(directory):
    texts = []
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), "r") as file:
            texts.append(file.read())
    return texts


def parse_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
    return "\n".join(pages)


def main():
    source_type = input("Enter the source type (url, folder, pdf): ").lower()
    if source_type == "url":
        url = input("Enter the URL: ")
        print(parse_url(url))
    elif source_type == "folder":
        directory = input("Enter the directory path: ")
        texts = parse_folder(directory)
        print("\n".join(texts))
    elif source_type == "pdf":
        pdf_file = input("Enter the PDF file path: ")
        print(parse_pdf(pdf_file))
    else:
        print("Invalid source type.")
