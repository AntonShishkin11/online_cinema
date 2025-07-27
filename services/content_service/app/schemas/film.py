
from pydantic import BaseModel
from typing import List, Optional

class FilmCard(BaseModel):
    slug: str
    title_localized: str
    poster_url: Optional[str]
    imdb_rating: Optional[float]
    year: Optional[int]

    class Config:
        orm_mode = True

class FilmDetail(FilmCard):
    title_original: Optional[str]
    short_description: Optional[str]
    full_description: Optional[str]
    country: Optional[str]
    duration: Optional[int]
    age_rating: Optional[str]
    trailer_url: Optional[str]
    quality: Optional[str]
