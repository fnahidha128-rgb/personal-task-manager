from fastapi import APIRouter, Depends, HTTPException

from schemas import TaskCreate
from database import (
    create_task,
    get_all_tasks,
    get_task_by_id,
    delete_task
)
from auth import get_current_user

router = APIRouter()


@router.post("/")
def add_task(
        task: TaskCreate,
        current_user: str = Depends(get_current_user)
):

    task_id = create_task(
        task.title,
        task.description,
        task.priority,
        task.due_date,
        current_user
    )

    return {
        "message": "Task created successfully",
        "task_id": task_id
    }


@router.get("/")
def all_tasks(
        current_user: str = Depends(get_current_user)
):

    tasks = get_all_tasks(current_user)

    return tasks


@router.get("/{task_id}")
def get_single_task(
        task_id: int,
        current_user: str = Depends(get_current_user)
):

    task = get_task_by_id(task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task["owner_email"] != current_user:
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    return task


@router.delete("/{task_id}")
def remove_task(
        task_id: int,
        current_user: str = Depends(get_current_user)
):

    task = get_task_by_id(task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task["owner_email"] != current_user:
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    delete_task(task_id)

    return {
        "message": "Task deleted successfully"
    }