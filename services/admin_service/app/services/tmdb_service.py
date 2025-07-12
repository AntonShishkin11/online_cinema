import os
import httpx
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BEARER_TOKEN = os.getenv("TMDB_BEARER_TOKEN")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

headers = {
    "Authorization": f"Bearer {TMDB_BEARER_TOKEN}",
    "accept": "application/json"
}

async def fetch_tmdb_movie(tmdb_id: int) -> dict:
    url = f"{TMDB_BASE_URL}/movie/{tmdb_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
