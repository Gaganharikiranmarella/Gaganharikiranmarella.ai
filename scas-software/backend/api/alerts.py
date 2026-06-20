from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from database.session import SessionLocal

from schemas.alert_schema import AlertCreate

from services.alert_service import AlertService


router = APIRouter(
    prefix="/api",
    tags=["Alerts"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/alerts")
def create_alert(
    payload: AlertCreate,
    db: Session = Depends(get_db)
):

    return AlertService.create_alert(
        db,
        payload
    )


@router.get("/alerts")
def get_alerts(
    db: Session = Depends(get_db)
):

    return AlertService.get_all(db)