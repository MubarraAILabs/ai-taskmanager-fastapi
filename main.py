from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from uuid import uuid4
app = FastAPI()
# -----------------------------
# Data Model
# -----------------------------
class Task(BaseModel):
    id: str = None
    title: str
    description: str = ""
    completed: bool = False
# In-memory storage
tasks: List[Task] = []
# -----------------------------
# Routes
# -----------------------------
@app.get("/")
def home():
    return {"message": "Task Manager API is running 🚀"}
# Get all tasks
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks
# Create a new task
@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    task.id = str(uuid4())
    tasks.append(task)
    return task
# Get single task
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")
# Update task
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, updated_task: Task):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            updated_task.id = task_id
            tasks[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")
# Delete task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(index)
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")
