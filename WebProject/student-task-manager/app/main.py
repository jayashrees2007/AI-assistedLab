from contextlib import asynccontextmanager
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Task


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Student Task Manager", lifespan=lifespan)


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    student_name: str = Field(min_length=1, max_length=100)


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    student_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    completed: Optional[bool] = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    student_name: str
    completed: bool


@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks(database: Session = Depends(get_db)):
    return database.scalars(select(Task).order_by(Task.id)).all()


@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, database: Session = Depends(get_db)):
    new_task = Task(**task.model_dump())
    database.add(new_task)
    database.commit()
    database.refresh(new_task)
    return new_task


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updates: TaskUpdate, database: Session = Depends(get_db)):
    task = database.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    for field, value in updates.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(task, field, value)
    database.commit()
    database.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, database: Session = Depends(get_db)):
    task = database.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    database.delete(task)
    database.commit()
