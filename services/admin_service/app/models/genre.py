
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

# Промежуточная таблица для связи many-to-many между FilmB2C и Genre
film_genre_association = Table(
    "film_genre_association",
    Base.metadata,
    Column("film_id", Integer, ForeignKey("films_b2c.id", ondelete="CASCADE")),
    Column("genre_id", Integer, ForeignKey("genres.id", ondelete="CASCADE")),
)

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    tmdb_id = Column(Integer, unique=True, nullable=False)

    films = relationship("FilmB2C", secondary=film_genre_association, back_populates="genres")