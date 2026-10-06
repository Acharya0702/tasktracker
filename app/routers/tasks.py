from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.task import TaskCreate, TaskRead, Status
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])

DB = Annotated[Session, Depends(get_db)]


def get_service(db: DB) -> TaskService:
    return TaskService(db)


Service = Annotated[TaskService, Depends(get_service)]


@router.get("", response_model=list[TaskRead])
def list_tasks(service: Service, status: Status | None = None):
    return service.list(status)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, service: Service):
    task = service.get(task_id)
    if task is None:
        raise HTTPException(404, "Task not found")
    return task


@router.post("", response_model=TaskRead, status_code=201)
def create_task(body: TaskCreate, service: Service):
    return service.create(body)