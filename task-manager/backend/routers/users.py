from fastapi import APIRouter

router = APIRouter()


@router.post("/register")
def register():
    return {"message": "register route"}


@router.post("/login")
def login():
    return {"message": "login route"}


@router.get("/me")
def me():
    return {"message": "current user"}