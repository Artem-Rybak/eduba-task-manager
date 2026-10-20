from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="EDUBA Task Manager API")

class Task(BaseModel):
    id: int
    title: str
    completed: bool = False

tasks_db = []

@app.post("/tasks/", response_model=Task, status_code=201)
def create_task(task: Task):
    if any(t.id == task.id for t in tasks_db):
        raise HTTPException(status_code=400, detail="Task ID already exists")
    tasks_db.append(task)
    return task

@app.get("/tasks/", response_model=List[Task])
def read_tasks(search: str = None):
    if search:
        return [t for t in tasks_db if search.lower() in t.title.lower()]
    return tasks_db

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    global tasks_db
    tasks_db = [t for t in tasks_db if t.id != task_id]
