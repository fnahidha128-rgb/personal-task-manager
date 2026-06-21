from fastapi import APIRouter, Depends, HTTPException

from schemas import TaskCreate, TaskUpdate, TaskStatus
from database import (
    create_task,
    get_all_tasks,
    get_task_by_id,
    delete_task,
    update_task,
    update_task_status,
    get_summary
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
@router.put("/{task_id}")
def edit_task(
        task_id: int,
        updated_task: TaskUpdate,
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

    update_task(
        task_id,
        updated_task.title,
        updated_task.description,
        updated_task.priority,
        updated_task.status,
        updated_task.due_date
    )

    return {
        "message": "Task updated successfully"
    }
@router.patch("/{task_id}/status")
def change_status(
        task_id: int,
        task_status: TaskStatus,
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

    update_task_status(
        task_id,
        task_status.status
    )

    return {
        "message": "Status updated successfully"
    }
@router.get("/summary")
def task_summary(
        current_user: str = Depends(get_current_user)
):

    summary = get_summary(current_user)

    return summary