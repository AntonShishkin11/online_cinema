
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.services.tmdb_service import fetch_tmdb_movie
from app.services.import_genres import import_genres_from_tmdb
from app.schemas.film_b2c import FilmCreate, FilmUpdate, FilmOut
from app.models.film_b2c import FilmB2C
from app.models.genre import Genre
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[FilmOut])
async def get_films(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FilmB2C).offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/{film_id}", response_model=FilmOut)
async def get_film(film_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FilmB2C).where(FilmB2C.id == film_id))
    film = result.scalar_one_or_none()
    if film is None:
        raise HTTPException(status_code=404, detail="Film not found")
    return film

@router.post("/", response_model=FilmOut, status_code=status.HTTP_201_CREATED)
async def create_film(film: FilmCreate, db: AsyncSession = Depends(get_db)):
    # Разделяем данные: genre_ids отдельно
    film_data = film.dict(exclude={"genre_ids"})
    genre_ids = film.genre_ids or []

    # Получаем объекты Genre по id
    genres = []
    if genre_ids:
        result = await db.execute(select(Genre).where(Genre.id.in_(genre_ids)))
        genres = result.scalars().all()

        if len(genres) != len(set(genre_ids)):
            raise HTTPException(status_code=400, detail="Некоторые жанры не найдены")

    # Создаём фильм и прикрепляем жанры
    new_film = FilmB2C(**film_data, genres=genres)

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
