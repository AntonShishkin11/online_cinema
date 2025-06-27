from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_movies():
    return [{"id": 1, "title": "Матрица", "year": 1999, "genre": "Фантастика", "video_url": "https://example.com/matrix.mp4"}]

@router.get("/{movie_id}")
def get_movie(movie_id: int):
    return {"id": movie_id, "title": "Матрица", "year": 1999, "genre": "Фантастика", "video_url": "https://example.com/matrix.mp4"}