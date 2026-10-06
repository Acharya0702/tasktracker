from datetime import date
from enum import StrEnum
from pydantic import BaseModel, Field


class Status(StrEnum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    priority: int = Field(ge=1, le=5)
    due_date: date | None = None


class TaskRead(TaskCreate):
    id: int
    status: Status