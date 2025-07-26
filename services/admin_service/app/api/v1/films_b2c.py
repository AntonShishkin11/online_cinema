from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from typing import List

from app.core.security import get_current_user_with_role
from app.services.tmdb_service import fetch_tmdb_movie, search_tmdb_movie_by_name
from app.services.import_genres import import_genres_from_tmdb
from app.schemas.film_b2c import FilmCreate, FilmUpdate, FilmOut
from app.models.film_b2c import FilmB2C
from app.models.genre import Genre
from app.db.session import get_db

router = APIRouter()


@router.get("/", response_model=List[FilmOut])
async def get_films(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(FilmB2C).where(FilmB2C.is_deleted == False).offset(skip).limit(limit)
    )
    return result.scalars().all()


@router.get("/fetch-tmdb")
async def fetch_tmdb_by_title(query: str):
    results = await search_tmdb_movie_by_name(query)
    if results.get("results"):
        return results["results"]
    raise HTTPException(status_code=404, detail="Фильм не найден в TMDb")


@router.get("/{film_id}", response_model=FilmOut)
async def get_film(film_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(FilmB2C).where(FilmB2C.id == film_id, FilmB2C.is_deleted == False)
    )
    film = result.scalar_one_or_none()
    if film is None:
        raise HTTPException(status_code=404, detail="Film not found")
    return film


@router.post("/", response_model=FilmOut, status_code=status.HTTP_201_CREATED)
async def create_film(
    film: FilmCreate,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_user_with_role(("admin", "moderator"))),
):
    film_data = film.dict(exclude={"genre_ids"})
    genre_ids = film.genre_ids or []

    # Проверка на ранее удалённый фильм
    stmt = select(FilmB2C).options(selectinload(FilmB2C.genres)).where(
        FilmB2C.title_localized == film_data["title_localized"],
        FilmB2C.year == film_data["year"],
        FilmB2C.country == film_data["country"],
        FilmB2C.is_deleted == True
    )
    result = await db.execute(stmt)
    existing_deleted_film = result.scalar_one_or_none()

    if existing_deleted_film:
        # "Воскрешаем" фильм
        for key, value in film_data.items():
            setattr(existing_deleted_film, key, value)
        existing_deleted_film.is_deleted = False

        # Обновляем жанры
        if genre_ids:
            result = await db.execute(select(Genre).where(Genre.id.in_(genre_ids)))
            genres = result.scalars().all()
            if len(genres) != len(set(genre_ids)):
                raise HTTPException(status_code=400, detail="Некоторые жанры не найдены")
            existing_deleted_film.genres = genres

        await db.commit()
        await db.refresh(existing_deleted_film)
        return existing_deleted_film

    # Иначе создаём новый
    new_film = FilmB2C(**film_data)
    if genre_ids:
        result = await db.execute(select(Genre).where(Genre.id.in_(genre_ids)))
        genres = result.scalars().all()
        if len(genres) != len(set(genre_ids)):
            raise HTTPException(status_code=400, detail="Некоторые жанры не найдены")
        new_film.genres = genres

    db.add(new_film)
    await db.commit()
    await db.refresh(new_film)
    return new_film


@router.put("/{film_id}", response_model=FilmOut)
async def update_film(
    film_id: int,
    film_update: FilmUpdate,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_user_with_role(("admin", "moderator")))
):
    result = await db.execute(
        select(FilmB2C)
        .where(FilmB2C.id == film_id, FilmB2C.is_deleted == False)
        .options(selectinload(FilmB2C.genres))
    )
    film = result.scalar_one_or_none()
    if film is None:
        raise HTTPException(status_code=404, detail="Film not found")

    update_data = film_update.dict(exclude_unset=True, exclude={"genre_ids"})
    for key, value in update_data.items():
        setattr(film, key, value)

    if film_update.genre_ids is not None:
        genre_ids = film_update.genre_ids
        result = await db.execute(select(Genre).where(Genre.id.in_(genre_ids)))
        genres = result.scalars().all()
        if len(genres) != len(set(genre_ids)):
            raise HTTPException(status_code=400, detail="Некоторые жанры не найдены")
        film.genres = genres

    await db.commit()
    await db.refresh(film)
    return film


@router.delete("/{film_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_film(
    film_id: int,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_user_with_role(("admin", "moderator")))
):
    result = await db.execute(
        select(FilmB2C).where(FilmB2C.id == film_id, FilmB2C.is_deleted == False)
    )
    film = result.scalar_one_or_none()
    if film is None:
        raise HTTPException(status_code=404, detail="Film not found")

    film.is_deleted = True
    await db.commit()
    return None


@router.post("/films/fetch_tmdb_data")
async def fetch_tmdb_data(
    tmdb_id: int,
    _: dict = Depends(get_current_user_with_role(("admin", "moderator")))
):
    try:
        data = await fetch_tmdb_movie(tmdb_id)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/genres/import")
async def import_genres(
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_user_with_role(("admin", "moderator")))
):
    await import_genres_from_tmdb(db)
    return {"message": "Жанры успешно импортированы"}
