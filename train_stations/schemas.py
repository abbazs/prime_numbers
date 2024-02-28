from pydantic import BaseModel
from typing import List, Optional

class TrainStationBase(BaseModel):
    arr: str
    dep: str
    day: int
    dist: int
    days: str

class TrainStationCreate(TrainStationBase):
    train_id: int
    station_id: int

class TrainStation(TrainStationBase):
    id: int
    station_id: int

    class Config:
        orm_mode = True

class TrainBase(BaseModel):
    number: str

class TrainCreate(TrainBase):
    pass

class Train(TrainBase):
    id: int
    stations: List[TrainStation] = []

    class Config:
        orm_mode = True

class StationBase(BaseModel):
    name: str

class StationCreate(StationBase):
    pass

class Station(StationBase):
    id: int
    trains: List[TrainStation] = []

    class Config:
        orm_mode = True
