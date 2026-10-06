from datetime import date
from enum import StrEnum
from pydantic import BaseModel, ConfigDict, Field


class Status(StrEnum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    priority: int = Field(ge=1, le=5)
    due_date: date | None = None


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=200)
    priority: int | None = Field(default=None, ge=1, le=5)
    status: Status | None = None
    due_date: date | None = None
    assignee_id: int | None = None


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    priority: int
    due_date: date | None
    status: Status
    project_id: int
    assignee_id: int | None