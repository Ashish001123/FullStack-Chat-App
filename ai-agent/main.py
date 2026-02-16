# from fastapi import FastAPI
# from pydantic import BaseModel
# from agent import run_agent

# app = FastAPI()

# class Query(BaseModel):
#     message: str

# @app.post("/chat")
# def chat(q: Query):
#     reply = run_agent(q.message)
#     return {"reply": reply}



from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are AI assistant for Chatty chat app."},
                {"role": "user", "content": req.message}
            ],
        )

        reply = response.choices[0].message.content if response.choices else "No response"

        return {"reply": reply}

    except Exception as e:
        print("AI ERROR:", e)
        return {"reply": "AI service error"}