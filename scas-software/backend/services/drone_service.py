from sqlalchemy.orm import Session

from database.models import DroneTelemetry
from database.models import Alert

from threat_engine.threat_assessor import ThreatAssessor
from swarm.clustering import SwarmDetector


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

        all_drones = db.query(
            DroneTelemetry
        ).all()

        swarm_detected = SwarmDetector.detect(
            all_drones
        )

        if swarm_detected:

            alert = Alert(
                severity="HIGH",
                message="Potential drone swarm detected"
            )

            db.add(alert)
            db.commit()

        return {
            "drone": drone,
            "threat_level": threat_level,
            "swarm_detected": swarm_detected
        }

    @staticmethod
    def get_all(
        db: Session
    ):

        return db.query(
            DroneTelemetry
        ).all()