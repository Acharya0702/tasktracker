from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.deps import CurrentUser, DB
from app.schemas.task import (
    Status,
    TaskAssign,
    TaskCreate,
    TaskRead,
    TaskUpdate,
)
from app.services.task_service import TaskService

router = APIRouter(tags=["tasks"])


def get_service(db: DB) -> TaskService:
    return TaskService(db)


Service = Annotated[TaskService, Depends(get_service)]


@router.get(
    "/projects/{project_id}/tasks",
    response_model=list[TaskRead],
)
def list_project_tasks(
    project_id: int,
    user: CurrentUser,
    service: Service,
    status: Status | None = None,
):
    return service.list_for_project(project_id, user.id, status)


@router.post(
    "/projects/{project_id}/tasks",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    project_id: int,
    body: TaskCreate,
    user: CurrentUser,
    service: Service,
):
    return service.create(project_id, user.id, body)


@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int, user: CurrentUser, service: Service):
    return service.get(task_id, user.id)


@router.patch("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    body: TaskUpdate,
    user: CurrentUser,
    service: Service,
):
    return service.update(task_id, user.id, body)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, user: CurrentUser, service: Service):
    service.delete(task_id, user.id)


@router.post("/tasks/{task_id}/assign", response_model=TaskRead)
def assign_task(
    task_id: int,
    body: TaskAssign,
    user: CurrentUser,
    service: Service,
):
    return service.assign(task_id, user.id, body.user_id)