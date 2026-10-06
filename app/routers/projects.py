from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.deps import CurrentUser
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.services.project_service import ProjectService

from app.deps import DB

router = APIRouter(prefix="/projects", tags=["projects"])


def get_service(db: DB) -> ProjectService:
    return ProjectService(db)


Service = Annotated[ProjectService, Depends(get_service)]


@router.get("", response_model=list[ProjectRead])
def list_projects(user: CurrentUser, service: Service):
    return service.list_for_owner(user.id)


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
    body: ProjectCreate, user: CurrentUser, service: Service
):
    return service.create(body, user.id)


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, user: CurrentUser, service: Service):
    return service.get_owned(project_id, user.id)


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: int,
    body: ProjectUpdate,
    user: CurrentUser,
    service: Service,
):
    return service.update(project_id, user.id, body)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, user: CurrentUser, service: Service):
    service.delete(project_id, user.id)