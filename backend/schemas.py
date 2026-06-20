from pydantic import BaseModel


# User Schemas
class UserRegister(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


# Task Schemas
class TaskCreate(BaseModel):
    title: str
    description: str
    priority: str
    due_date: str


class TaskUpdate(BaseModel):
    title: str
    description: str
    priority: str
    status: str
    due_date: str


class TaskStatus(BaseModel):
    status: str


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    status: str
    due_date: str
    owner_email: str