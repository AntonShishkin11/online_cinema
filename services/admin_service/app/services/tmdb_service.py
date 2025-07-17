import os
import httpx
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.film_b2c import FilmB2C
from app.models.genre import Genre
from app.schemas.film_b2c import FilmCreate

load_dotenv()

TMDB_BEARER_TOKEN = os.getenv("TMDB_BEARER_TOKEN")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

headers = {
    "Authorization": f"Bearer {TMDB_BEARER_TOKEN}",
    "accept": "application/json"
}


async def search_tmdb_movie_by_name(query: str) -> dict:
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {"query": query}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

async def fetch_tmdb_movie(tmdb_id: int) -> dict:
    url = f"{TMDB_BASE_URL}/movie/{tmdb_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()



# async def import_tmdb_film_to_db(tmdb_id: int, db: AsyncSession): Пока не нужна
#     data = await fetch_tmdb_movie(tmdb_id)
#
#     # Получаем жанры по внешним TMDb ID
#     genre_ids = [genre["id"] for genre in data.get("genres", [])]
#     genres = []
#     if genre_ids:
#         result = await db.execute(select(Genre).where(Genre.tmdb_id.in_(genre_ids)))
#         genres = result.scalars().all()
#
#     # Собираем данные
#     film_data = FilmCreate(
#         title_localized=data["title"],
#         title_original=data.get("original_title"),
#         short_description=data.get("tagline"),
#         full_description=data.get("overview"),
#         year=int(data.get("release_date", "0000")[:4]) if data.get("release_date") else None,
#         country=",".join([c["name"] for c in data.get("production_countries", [])]),
#         age_rating=None,
#         imdb_rating=data.get("vote_average"),
#         poster_url=f"https://image.tmdb.org/t/p/w500{data['poster_path']}" if data.get("poster_path") else None,
#         genre_ids=genre_ids
#     )
#
#     # Создаём фильм
#     new_film = FilmB2C(**film_data.dict(exclude={"genre_ids"}), genres=genres)
#
#     db.add(new_film)
#     await db.commit()
#     await db.refresh(new_film)
#     return new_film
