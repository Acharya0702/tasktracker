from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, Status


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def list_for_project(
        self, project_id: int, status: Status | None = None
    ) -> list[Task]:
        stmt = select(Task).where(Task.project_id == project_id)
        if status:
            stmt = stmt.where(Task.status == status)
        return list(self.db.scalars(stmt))

    def get(self, task_id: int) -> Task | None:
        return self.db.get(Task, task_id)

    def create(self, project_id: int, data: TaskCreate) -> Task:
        task = Task(**data.model_dump(), project_id=project_id)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update(self, task_id: int, data: TaskUpdate) -> Task | None:
        task = self.get(task_id)
        if task is None:
            return None
        updates = data.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(task, field, value)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task_id: int) -> bool:
        task = self.get(task_id)
        if task is None:
            return False
        self.db.delete(task)
        self.db.commit()
        return True