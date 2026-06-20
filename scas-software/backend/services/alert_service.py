from sqlalchemy.orm import Session

from database.models import Alert

from websocket.manager import manager

import asyncio


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

        try:

            asyncio.create_task(
                manager.broadcast(
                    {
                        "type": "alert",
                        "severity": alert.severity,
                        "message": alert.message
                    }
                )
            )

        except:
            pass

        return alert

    @staticmethod
    def get_all(
        db: Session
    ):

        return db.query(
            Alert
        ).all()