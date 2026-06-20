from sqlalchemy.orm import Session

from database.models import DroneTelemetry

from threat_engine.threat_assessor import ThreatAssessor


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

        threat_level = ThreatAssessor.assess(
            drone
        )

        return {
            "drone": drone,
            "threat_level": threat_level
        }

    @staticmethod
    def get_all(
        db: Session
    ):

        return db.query(
            DroneTelemetry
        ).all()