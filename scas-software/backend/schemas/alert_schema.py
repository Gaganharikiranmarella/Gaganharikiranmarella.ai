from pydantic import BaseModel


class AlertCreate(BaseModel):
    severity: str
    message: str