from fastapi import FastAPI
from app.routers import projects, tasks

app = FastAPI(title="Task Tracker")

app.include_router(projects.router)
app.include_router(tasks.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}