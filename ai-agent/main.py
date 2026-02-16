from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_agent

app = FastAPI()

class Query(BaseModel):
    message: str

@app.post("/chat")
def chat(q: Query):
    reply = run_agent(q.message)
    return {"reply": reply}