from fastapi import FastAPI
from fastapi import WebSocket
from fastapi.middleware.cors import CORSMiddleware

from database.models import Base
from database.session import engine

from api.drones import router as drone_router
from api.alerts import router as alert_router
from api.test import router as test_router

from websocket.manager import manager


Base.metadata.create_all(
    bind=engine
)

app = FastAPI(
    title="SCAS Backend"
)

# Configure CORS so the React app can communicate with the backend locally
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    drone_router
)

app.include_router(
    alert_router
)

app.include_router(
    test_router
)


@app.get("/")
def home():

    return {
        "message": "SCAS Backend Running"
    }


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket
):

    await manager.connect(
        websocket
    )

    try:

        while True:

            await websocket.receive_text()

    except:

        manager.disconnect(
            websocket
        )