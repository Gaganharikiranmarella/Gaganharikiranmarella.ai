from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime

from sqlalchemy.orm import declarative_base

from datetime import datetime

Base = declarative_base()


class DroneTelemetry(Base):

    __tablename__ = "drone_telemetry"

    id = Column(Integer, primary_key=True)

    drone_uid = Column(String)

    latitude = Column(Float)

    longitude = Column(Float)

    altitude = Column(Float)

    velocity = Column(Float)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )


class Alert(Base):

    __tablename__ = "alerts"

    id = Column(
        Integer,
        primary_key=True
    )

    severity = Column(String)

    message = Column(String)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )