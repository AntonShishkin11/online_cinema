from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.services.tmdb_service import fetch_tmdb_movie, search_tmdb_movie_by_name
from app.services.import_genres import import_genres_from_tmdb
from app.schemas.film_b2c import FilmCreate, FilmUpdate, FilmOut
from app.models.film_b2c import FilmB2C
from app.models.genre import Genre
from app.db.session import get_db, get_async_sessionmaker

router = APIRouter()

@router.get("/", response_model=List[FilmOut])
async def get_films(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FilmB2C).offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/fetch-tmdb")
async def fetch_tmdb_by_title(query: str):
    results = await search_tmdb_movie_by_name(query)
    if results.get("results"):
        return results["results"]
    raise HTTPException(status_code=404, detail="Фильм не найден в TMDb")

@router.get("/{film_id}", response_model=FilmOut)
async def get_film(film_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FilmB2C).where(FilmB2C.id == film_id))
    film = result.scalar_one_or_none()
    if film is None:
        raise HTTPException(status_code=404, detail="Film not found")
    return film

@router.post("/", response_model=FilmOut, status_code=status.HTTP_201_CREATED)
async def create_film(film: FilmCreate, db: AsyncSession = Depends(get_db)):
    film_data = film.dict(exclude={"genre_ids"})
    genre_ids = film.genre_ids or []

    genres = []
    if genre_ids:
        result = await db.execute(select(Genre).where(Genre.id.in_(genre_ids)))
        genres = result.scalars().all()
        if len(genres) != len(set(genre_ids)):
            raise HTTPException(status_code=400, detail="Некоторые жанры не найдены")

    new_film = FilmB2C(**film_data)
    new_film.genres = genres

    db.add(new_film)
    await db.commit()
    await db.refresh(new_film)
    return new_film

@router.put("/{film_id}", response_model=FilmOut)
async def update_film(film_id: int, film_update: FilmUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FilmB2C).where(FilmB2C.id == film_id))
    film = result.scalar_one_or_none()
    if film is None:
        raise HTTPException(status_code=404, detail="Film not found")
    for key, value in film_update.dict(exclude_unset=True).items():
        setattr(film, key, value)
    await db.commit()
    await db.refresh(film)
    return film

@router.delete("/{film_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_film(film_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FilmB2C).where(FilmB2C.id == film_id))
    film = result.scalar_one_or_none()
    if film is None:
        raise HTTPException(status_code=404, detail="Film not found")
    await db.delete(film)
    await db.commit()
    return None

@router.post("/films/fetch_tmdb_data")
async def fetch_tmdb_data(tmdb_id: int):
    try:
        data = await fetch_tmdb_movie(tmdb_id)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/genres/import", summary="Импортировать жанры из TMDb")
async def import_genres(db: AsyncSession = Depends(get_db)):
    await import_genres_from_tmdb(db)
    return {"message": "Жанры успешно импортированы"}



# @router.post("/import-tmdb", response_model=FilmOut) Не требуется поиск по tmdb_id
# async def import_film_from_tmdb(tmdb_id: int, db: AsyncSession = Depends(get_db)):
#     try:
#         data = await fetch_tmdb_movie(tmdb_id)
#
#         genre_ids = [genre["id"] for genre in data.get("genres", [])]
#         genres = []
#         if genre_ids:
#             result = await db.execute(select(Genre).where(Genre.tmdb_id.in_(genre_ids)))
#             genres = result.scalars().all()
#
#         film_data = {
#             "title_localized": data["title"],
#             "title_original": data.get("original_title"),
#             "short_description": data.get("tagline"),
#             "full_description": data.get("overview"),
#             "year": int(data.get("release_date", "0000")[:4]) if data.get("release_date") else None,
#             "country": ",".join([c["name"] for c in data.get("production_countries", [])]),
#             "age_rating": None,
#             "imdb_rating": data.get("vote_average"),
#             "poster_url": f"https://image.tmdb.org/t/p/w500{data['poster_path']}" if data.get("poster_path") else None,
#         }
#
#         new_film = FilmB2C(**film_data)
#         new_film.genres = genres
#
#         db.add(new_film)
#         await db.commit()
#         await db.refresh(new_film)
#         return new_film
#
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


