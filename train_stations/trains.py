from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from train_stations import models, schemas
import traceback
import os
import subprocess

router = APIRouter(prefix="/trains", tags=["trains"])


def get_db():
    db = models.Session()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[schemas.Train])
def read_trains(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        trains = db.query(models.Train).offset(skip).limit(limit).all()
        return trains
    except Exception as e:
        return {
            "error": str(e),
            "details": traceback.format_exc(),
            "pwd": os.curdir,
            "files": os.system("ls -lart"),
        }


@router.get("/init_db")
def create_database():
    models.Base.metadata.create_all(bind=models.engine)
    models.add_trains_from_json("trains.json")
