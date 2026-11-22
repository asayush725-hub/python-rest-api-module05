from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, status

from auth import verify_api_key
from database import (
    create_task,
    delete_task,
    get_all_tasks,
    get_task_by_id,
    init_db,
    update_task,
)
from schemas import TaskCreate, TaskResponse, TaskUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Task Manager REST API",
    description="Module 05 REST API with FastAPI, SQLite, schema validation, and API key auth.",
    version="1.0.0",
    lifespan=lifespan,
)


def _format_task(row: dict) -> TaskResponse:
    return TaskResponse(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        completed=bool(row["completed"]),
    )


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "API is running"}


@app.get(
    "/tasks",
    response_model=list[TaskResponse],
    tags=["Tasks"],
    dependencies=[Depends(verify_api_key)],
)
def list_tasks():
    rows = get_all_tasks()
    return [_format_task(r) for r in rows]


@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["Tasks"],
    dependencies=[Depends(verify_api_key)],
)
def read_task(task_id: int):
    row = get_task_by_id(task_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return _format_task(row)


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Tasks"],
    dependencies=[Depends(verify_api_key)],
)
def add_task(payload: TaskCreate):
    row = create_task(title=payload.title, description=payload.description)
    return _format_task(row)


@app.put(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["Tasks"],
    dependencies=[Depends(verify_api_key)],
)
def edit_task(task_id: int, payload: TaskUpdate):
    row = update_task(
        task_id=task_id,
        title=payload.title,
        description=payload.description,
        completed=payload.completed,
    )
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return _format_task(row)


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Tasks"],
    dependencies=[Depends(verify_api_key)],
)
def remove_task(task_id: int):
    deleted = delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")