from fastapi import APIRouter

router = APIRouter()

@router.post("/register")
def register():
    return {"msg": "User registered"}

@router.post("/login")
def login():
    return {"msg": "User logged in"}