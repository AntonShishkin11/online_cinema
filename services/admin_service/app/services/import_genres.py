
import httpx
import os
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.genre import Genre
from sqlalchemy.future import select
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BEARER_TOKEN = os.getenv("TMDB_BEARER_TOKEN")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

headers = {
    "Authorization": f"Bearer {TMDB_BEARER_TOKEN}",
    "accept": "application/json"
}

async def import_genres_from_tmdb(db: AsyncSession):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TMDB_BASE_URL}/genre/movie/list", headers=headers)
        response.raise_for_status()
        data = response.json()
        genres = data.get("genres", [])

    existing_genres = await db.execute(select(Genre))
    existing_names = {genre.name for genre in existing_genres.scalars()}

    for genre_data in genres:
        if genre_data["name"] not in existing_names:
            genre = Genre(name=genre_data["name"], tmdb_id=genre_data["id"])
            db.add(genre)

    await db.commit()
