from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from train_stations import models, schemas  # Adjust the import paths as necessary


router = APIRouter(prefix="/trains", tags=["trains"])


def get_db():
    db = models.Session()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[schemas.Train])
def read_trains(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    trains = db.query(models.Train).offset(skip).limit(limit).all()
    return trains

@router.get("/init_db")
def create_database():
    models.Base.metadata.create_all(bind=models.engine)
    models.add_trains_from_json("trains.json")
