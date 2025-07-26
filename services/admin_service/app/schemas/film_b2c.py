from typing import List, Optional
from pydantic import BaseModel, Field

class FilmBase(BaseModel):
    title_localized: str
    title_original: Optional[str] = None
    short_description: Optional[str] = None
    full_description: Optional[str] = None
    genre_ids: Optional[List[int]] = Field(default_factory=list)
    country: Optional[str] = None
    year: Optional[int] = None
    duration: Optional[int] = None
    age_rating: Optional[str] = None
    trailer_url: Optional[str] = None
    poster_url: Optional[str] = None
    imdb_rating: Optional[float] = None
    is_new: Optional[bool] = False
    is_exclusive: Optional[bool] = False
    is_available: Optional[bool] = True
    quality: Optional[str] = None

class FilmCreate(FilmBase):
    pass

class FilmUpdate(FilmBase):
    pass

class FilmOut(FilmBase):
    id: int
    is_deleted: bool

    class Config:
        orm_mode = True
