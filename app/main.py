from fastapi import FastAPI, Depends, HTTPException, status, Response
from .database import Base, engine
from . import models, schemas, database
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List


Base.metadata.create_all(bind=engine)
app = FastAPI()
class Task(BaseModel):
    id: int
    title: str
    description: str


@app.get("/")
def root():
    return {"message": "Task Tracker API is running"}

@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks/", response_model=List[schemas.Task])
def get_tasks(db: Session = Depends(database.get_db)):
    tasks = db.query(models.Task).all()
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(database.get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}/", response_model=schemas.Task)
def update_task(task_id: int, update_task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = update_task.title
    task.description = update_task.description
    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(database.get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return Response(status_code=204)