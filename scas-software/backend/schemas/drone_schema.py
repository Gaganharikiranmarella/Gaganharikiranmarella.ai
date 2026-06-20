from pydantic import BaseModel

class DroneCreate(BaseModel):
    drone_uid: str
    latitude: float
    longitude: float
    altitude: float
    velocity: float