import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()


def build_data_client():
    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        raise RuntimeError("YOUTUBE_API_KEY not set. Copy .env.example to .env and fill it in.")
    return build("youtube", "v3", developerKey=api_key, cache_discovery=False)
