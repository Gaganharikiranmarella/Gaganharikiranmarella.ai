from sqlalchemy.orm import Session

from database.models import DroneTelemetry


class DroneService:

    @staticmethod
    def create_drone(
        db: Session,
        payload
    ):

        drone = DroneTelemetry(
            drone_uid=payload.drone_uid,
            latitude=payload.latitude,
            longitude=payload.longitude,
            altitude=payload.altitude,
            velocity=payload.velocity
        )

        db.add(drone)
        db.commit()
        db.refresh(drone)

        return drone

    @staticmethod
    def get_all(
        db: Session
    ):

        return db.query(
            DroneTelemetry
        ).all()