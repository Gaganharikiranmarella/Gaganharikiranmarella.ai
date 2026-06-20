from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from database.session import SessionLocal
from services.drone_service import DroneService
from schemas.drone_schema import DroneCreate


router = APIRouter(
    prefix="/api",
    tags=["Drones"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/drones")
def create_drone(
    payload: DroneCreate,
    db: Session = Depends(get_db)
):

    return DroneService.create_drone(
        db,
        payload
    )


@router.get("/drones")
def get_drones(
    db: Session = Depends(get_db)
):

    return DroneService.get_all(db)