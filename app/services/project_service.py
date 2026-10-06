from sqlalchemy import select
from sqlalchemy.orm import Session

from app.errors import ForbiddenError, NotFoundError
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(self, db: Session):
        self.db = db

    def list_for_owner(self, owner_id: int) -> list[Project]:
        stmt = select(Project).where(Project.owner_id == owner_id)
        return list(self.db.scalars(stmt))

    def get_owned(self, project_id: int, owner_id: int) -> Project:
        project = self.db.get(Project, project_id)
        if project is None:
            raise NotFoundError("Project", project_id)
        if project.owner_id != owner_id:
            # Return 404 (not 403) to avoid leaking existence
            raise NotFoundError("Project", project_id)
        return project

    def create(self, data: ProjectCreate, owner_id: int) -> Project:
        project = Project(**data.model_dump(), owner_id=owner_id)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def update(
        self, project_id: int, owner_id: int, data: ProjectUpdate
    ) -> Project:
        project = self.get_owned(project_id, owner_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(project, field, value)
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, project_id: int, owner_id: int) -> None:
        project = self.get_owned(project_id, owner_id)
        self.db.delete(project)
        self.db.commit()