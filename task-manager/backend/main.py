from fastapi import FastAPI
from backend.database import init_db
from backend.routers import users, tasks

app = FastAPI()


@app.on_event("startup")
def startup():
    init_db()


app.include_router(users.router, prefix="/auth", tags=["Auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])


@app.get("/")
def home():
    return {"message": "Task Manager API"}