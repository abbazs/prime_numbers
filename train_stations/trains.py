from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any, List
from train_stations import models, schemas
import traceback
from pathlib import Path
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
        result = subprocess.run(["ls", "-lart"], capture_output=True, text=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "details": traceback.format_exception(e),
                "pwd": str(Path(__file__)),
                "files": result.stdout.split("\n"),
            },
        )


@router.get("/init_db")
def create_database():
    models.Base.metadata.create_all(bind=models.engine)
    models.add_trains_from_json("trains.json")
