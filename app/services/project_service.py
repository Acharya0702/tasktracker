from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(self, db: Session):
        self.db = db

    def list_for_owner(self, owner_id: int) -> list[Project]:
        stmt = select(Project).where(Project.owner_id == owner_id)
        return list(self.db.scalars(stmt))

    def get(self, project_id: int) -> Project | None:
        return self.db.get(Project, project_id)

    def create(self, data: ProjectCreate, owner_id: int = 1) -> Project:
        project = Project(**data.model_dump(), owner_id=owner_id)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def update(self, project_id: int, data: ProjectUpdate) -> Project | None:
        project = self.get(project_id)
        if project is None:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(project, field, value)
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, project_id: int) -> bool:
        project = self.get(project_id)
        if project is None:
            return False
        self.db.delete(project)
        self.db.commit()
        return True