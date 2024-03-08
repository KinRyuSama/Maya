import dotenv
import openai
import os

dotenv.load_dotenv(override=True)
openai.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
openai.api_key = os.getenv("OPENAI_API_KEY")


class AppConfig:
    pass
