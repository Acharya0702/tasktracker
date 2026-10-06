from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])

DB = Annotated[Session, Depends(get_db)]


def get_service(db: DB) -> ProjectService:
    return ProjectService(db)


Service = Annotated[ProjectService, Depends(get_service)]


@router.get("", response_model=list[ProjectRead])
def list_projects(service: Service):
    # TODO: Day 10 ରେ current_user ଆସିବ
    return service.list_for_owner(owner_id=1)


@router.post("", response_model=ProjectRead, status_code=201)
def create_project(body: ProjectCreate, service: Service):
    # TODO: Day 10 ରେ current_user ଆସିବ
    return service.create(body, owner_id=1)


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, service: Service):
    project = service.get(project_id)
    if project is None:
        raise HTTPException(404, "Project not found")
    return project


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(project_id: int, body: ProjectUpdate, service: Service):
    project = service.update(project_id, body)
    if project is None:
        raise HTTPException(404, "Project not found")
    return project


@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int, service: Service):
    if not service.delete(project_id):
        raise HTTPException(404, "Project not found")