from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, Status


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def list(self, status: Status | None = None) -> list[Task]:
        stmt = select(Task)
        if status:
            stmt = stmt.where(Task.status == status)
        return list(self.db.scalars(stmt))

    def get(self, task_id: int) -> Task | None:
        return self.db.get(Task, task_id)

    def create(self, data: TaskCreate) -> Task:
        task = Task(**data.model_dump(), project_id=1)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task