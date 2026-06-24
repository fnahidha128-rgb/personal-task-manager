from pydantic import BaseModel


# ================= USERS =================

class UserRegister(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


# ================= TASKS =================

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


# ================= SUMMARY =================

class SummaryResponse(BaseModel):
    status: str
    count: int