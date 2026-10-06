from app.schemas.task import TaskCreate, Status


class TaskService:
    def __init__(self):
        # Temporary in-memory storage (Day 5 ରେ database ଆସିବ)
        self._tasks: dict[int, dict] = {
            1: {"id": 1, "title": "Prepare FastAPI interview", "status": "todo", "priority": 2, "due_date": None},
            2: {"id": 2, "title": "Build Task Tracker API", "status": "doing", "priority": 3, "due_date": None},
            3: {"id": 3, "title": "Write tests", "status": "done", "priority": 1, "due_date": None},
        }
        self._next_id = 4

    def list(self, status: Status | None = None) -> list[dict]:
        items = list(self._tasks.values())
        if status:
            items = [t for t in items if t["status"] == status]
        return items

    def get(self, task_id: int) -> dict:
        return self._tasks[task_id]

    def create(self, data: TaskCreate) -> dict:
        new_task = {
            "id": self._next_id,
            "title": data.title,
            "priority": data.priority,
            "due_date": data.due_date,
            "status": "todo",
        }
        self._tasks[self._next_id] = new_task
        self._next_id += 1
        return new_task