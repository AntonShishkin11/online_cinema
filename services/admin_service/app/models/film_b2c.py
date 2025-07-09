from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ARRAY
from sqlalchemy.sql import func
from app.db.session import Base  # ✅ общий Base

class FilmB2C(Base):
    __tablename__ = "films_b2c"

    id = Column(Integer, primary_key=True, index=True)
    title_localized = Column(String, nullable=False)
    title_original = Column(String)
    short_description = Column(String)
    full_description = Column(String)
    genres = Column(ARRAY(String))
    country = Column(String)
    year = Column(Integer)
    duration = Column(Integer)
    age_rating = Column(String)
    trailer_url = Column(String)
    poster_url = Column(String)
    imdb_rating = Column(Float)
    is_new = Column(Boolean, default=False)
    is_exclusive = Column(Boolean, default=False)
    is_available = Column(Boolean, default=True)
    quality = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
