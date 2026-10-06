from sqlalchemy import select
from sqlalchemy.orm import Session

from app.errors import NotFoundError
from app.models.project import Project
from app.models.task import Task
from app.models.user import User
from app.schemas.task import Status, TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def _get_owned_project(self, project_id: int, owner_id: int) -> Project:
        project = self.db.get(Project, project_id)
        if project is None or project.owner_id != owner_id:
            raise NotFoundError("Project", project_id)
        return project

    def _get_owned_task(self, task_id: int, owner_id: int) -> Task:
        task = self.db.get(Task, task_id)
        if task is None:
            raise NotFoundError("Task", task_id)
        # Check that the project belongs to the user
        project = self.db.get(Project, task.project_id)
        if project is None or project.owner_id != owner_id:
            raise NotFoundError("Task", task_id)
        return task

    def list_for_project(
        self,
        project_id: int,
        owner_id: int,
        status: Status | None = None,
    ) -> list[Task]:
        self._get_owned_project(project_id, owner_id)
        stmt = select(Task).where(Task.project_id == project_id)
        if status:
            stmt = stmt.where(Task.status == status)
        return list(self.db.scalars(stmt))

    def get(self, task_id: int, owner_id: int) -> Task:
        return self._get_owned_task(task_id, owner_id)

    def create(
        self, project_id: int, owner_id: int, data: TaskCreate
    ) -> Task:
        self._get_owned_project(project_id, owner_id)
        task = Task(**data.model_dump(), project_id=project_id)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update(
        self, task_id: int, owner_id: int, data: TaskUpdate
    ) -> Task:
        task = self._get_owned_task(task_id, owner_id)
        if data.assignee_id is not None:
            self._get_assignee(data.assignee_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(task, field, value)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task_id: int, owner_id: int) -> None:
        task = self._get_owned_task(task_id, owner_id)
        self.db.delete(task)
        self.db.commit()

    def assign(self, task_id: int, owner_id: int, user_id: int) -> Task:
        task = self._get_owned_task(task_id, owner_id)
        self._get_assignee(user_id)
        task.assignee_id = user_id
        self.db.commit()
        self.db.refresh(task)
        return task

    def _get_assignee(self, user_id: int) -> User:
        user = self.db.get(User, user_id)
        if user is None:
            raise NotFoundError("User", user_id)
        return user
