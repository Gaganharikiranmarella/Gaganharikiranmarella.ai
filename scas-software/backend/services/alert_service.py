from sqlalchemy.orm import Session

from database.models import Alert


class AlertService:

    @staticmethod
    def create_alert(
        db: Session,
        payload
    ):

        alert = Alert(
            severity=payload.severity,
            message=payload.message
        )

        db.add(alert)
        db.commit()
        db.refresh(alert)

        return alert

    @staticmethod
    def get_all(
        db: Session
    ):

        return db.query(
            Alert
        ).all()