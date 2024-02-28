from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
import json

Base = declarative_base()


class TrainStation(Base):
    __tablename__ = "train_stations"
    id = Column(Integer, primary_key=True)
    train_id = Column(Integer, ForeignKey("trains.id"))
    station_id = Column(Integer, ForeignKey("stations.id"))
    arr = Column(String)
    dep = Column(String)
    day = Column(Integer)
    dist = Column(Integer)
    train = relationship("Train", back_populates="stations")
    station = relationship("Station", back_populates="trains")
    days = Column(String)


class Train(Base):
    __tablename__ = "trains"
    id = Column(Integer, primary_key=True)
    number = Column(String, unique=True)
    stations = relationship(
        "TrainStation", order_by=TrainStation.id, back_populates="train"
    )


class Station(Base):
    __tablename__ = "stations"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    trains = relationship(
        "TrainStation", order_by=TrainStation.id, back_populates="station"
    )


# Create the engine and tables
engine = create_engine("sqlite:///trains_stations.sqlite3")

Session = sessionmaker(bind=engine)



def get_day_name(start_day, day_offset):
    days_of_week = ["M", "Tu", "W", "Th", "F", "Sa", "Su"]

    # Find the index of the start_day in the days_of_week list
    start_index = days_of_week.index(start_day)

    # Calculate the new index with day_offset, wrapping around using modulo by the number of days in a week
    new_index = (start_index + day_offset - 1) % len(days_of_week)

    # Return the day name at the new index
    return days_of_week[new_index]


def add_trains_from_json(file_path):
    Base.metadata.create_all(engine)
    session = Session()

    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
    
    with open(file_path, "r") as f:
        trains_json = json.load(f)
    
    for train_number, train_details in trains_json.items():
        train = Train(number=train_number)
        session.add(train)
        session.flush()  # This is to ensure train.id is available immediately
        start_days = train_details["days"]
        for station_name, station_details in train_details["stations"].items():
            station = session.query(Station).filter_by(name=station_name).first()
            if not station:
                station = Station(name=station_name)
                session.add(station)
                session.flush()  # Ensure station.id is available

            train_station = TrainStation(
                train_id=train.id,
                station_id=station.id,
                arr=station_details["arr"],
                dep=station_details["dep"],
                day=(d := int(station_details["day"])),
                dist=int(station_details["dist"]),
                days=",".join(
                    [get_day_name(start_day=s, day_offset=d) for s in start_days]
                ),
            )
            session.add(train_station)
        session.commit()
