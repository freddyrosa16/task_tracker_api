from fastapi import FastAPI, Depends
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
def get_task(db: Session = Depends(database.get_db)):
    tasks = db.query(models.Task).all()
    return tasks