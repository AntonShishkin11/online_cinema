
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.models.film_b2c import FilmB2C
from app.schemas.film import FilmCard, FilmDetail

router = APIRouter()

@router.get("/movies", response_model=list[FilmCard])
async def get_movies(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FilmB2C).where(FilmB2C.is_deleted == False))
    films = result.scalars().all()
    return films

@router.get("/movies/{slug}", response_model=FilmDetail)
async def get_movie_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FilmB2C).where(FilmB2C.slug == slug))
    film = result.scalar_one_or_none()
    if not film:
        raise HTTPException(status_code=404, detail="Movie not found")
    return film
