from fastapi import FastAPI

from database.models import Base
from database.session import engine

from api.drones import router as drone_router


Base.metadata.create_all(
    bind=engine
)

app = FastAPI(
    title="SCAS Backend"
)


app.include_router(
    drone_router
)


@app.get("/")
def home():

    return {
        "message": "SCAS Backend Running"
    }
