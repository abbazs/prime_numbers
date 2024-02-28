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


@router.post("/", response_model=schemas.Train)
def create_train(train: schemas.TrainCreate, db: Session = Depends(get_db)):
    db_train = models.Train(**train.model_dump())
    db.add(db_train)
    db.commit()
    db.refresh(db_train)
    return db_train


@router.put("/{train_id}", response_model=schemas.Train)
def update_train(train_id: int, train: schemas.Train, db: Session = Depends(get_db)):
    db_train = db.query(models.Train).filter(models.Train.id == train_id).first()
    if not db_train:
        raise HTTPException(status_code=404, detail="Train not found")
    for key, value in train.model_dump().items():
        setattr(db_train, key, value)
    db.commit()
    return db_train


@router.get("/", response_model=List[schemas.Train])
def read_trains(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    trains = db.query(models.Train).offset(skip).limit(limit).all()
    return trains

@router.get("/init_db")
def create_database():
    models.Base.metadata.create_all(bind=models.engine)
    models.add_trains_from_json("trains.json")
