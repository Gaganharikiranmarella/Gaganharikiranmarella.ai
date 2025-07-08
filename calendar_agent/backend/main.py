# backend/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .langchain_agent import run_agent

app = FastAPI()

# Allow frontend (Streamlit) to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        message = body.get("message", "")
        if not message:
            return {"response": "No message received."}

        reply = run_agent(message)
        return {"response": reply or "I couldn't generate a reply."}
    except Exception as e:
        return {"response": f"Internal server error: {str(e)}"}
