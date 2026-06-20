from fastapi import APIRouter

router = APIRouter()


@router.post("/")
def create_task():
    return {"message": "create task"}


@router.get("/")
def get_tasks():
    return {"message": "all tasks"}


@router.get("/{task_id}")
def get_task(task_id: int):
    return {"task_id": task_id}


@router.put("/{task_id}")
def update_task(task_id: int):
    return {"task_id": task_id}


@router.patch("/{task_id}/status")
def update_status(task_id: int):
    return {"task_id": task_id}


@router.delete("/{task_id}")
def delete_task(task_id: int):
    return {"task_id": task_id}


@router.get("/summary")
def summary():
    return {"summary": "task summary"}