from pydantic import BaseModel, Field, computed_field
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


class Stations(TrainStationBase):
    station_: "Station" = Field(..., alias="station", exclude=True)

    @computed_field(return_type=str)
    @property
    def station(self):
        return self.station_.name

    class Config:
        from_attributes = True


class TrainBase(BaseModel):
    number: str


class TrainCreate(TrainBase):
    pass


class Train(TrainBase):
    number: int
    stations: List["Stations"] = []

    class Config:
        from_attributes = True


class StationBase(BaseModel):
    name: str


class StationCreate(StationBase):
    pass


class Station(StationBase):
    name: str
    # trains: List[TrainStation] = []

    class Config:
        from_attributes = True


Train.model_rebuild()
Station.model_rebuild()
Stations.model_rebuild()
