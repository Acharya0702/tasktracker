from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate, Status
from app.services.task_service import TaskService

router = APIRouter(tags=["tasks"])

DB = Annotated[Session, Depends(get_db)]


def get_service(db: DB) -> TaskService:
    return TaskService(db)


Service = Annotated[TaskService, Depends(get_service)]


# Project-scoped tasks
@router.get("/projects/{project_id}/tasks", response_model=list[TaskRead])
def list_project_tasks(
    project_id: int,
    service: Service,
    status: Status | None = None,
):
    return service.list_for_project(project_id, status)


@router.post(
    "/projects/{project_id}/tasks",
    response_model=TaskRead,
    status_code=201,
)
def create_task(project_id: int, body: TaskCreate, service: Service):
    return service.create(project_id, body)


# Direct task endpoints
@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int, service: Service):
    task = service.get(task_id)
    if task is None:
        raise HTTPException(404, "Task not found")
    return task


@router.patch("/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: int, body: TaskUpdate, service: Service):
    task = service.update(task_id, body)
    if task is None:
        raise HTTPException(404, "Task not found")
    return task


@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, service: Service):
    if not service.delete(task_id):
        raise HTTPException(404, "Task not found")