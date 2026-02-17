# from fastapi import FastAPI
# from pydantic import BaseModel
# from dotenv import load_dotenv
# from pathlib import Path
# import os
# from openai import OpenAI

# env_path = Path(__file__).parent / ".env"
# load_dotenv(dotenv_path=env_path)

# api_key = os.getenv("GROQ_API_KEY")

# if not api_key:
#     raise ValueError("❌ GROQ_API_KEY missing in .env")

# client = OpenAI(
#     api_key=api_key,
#     base_url="https://api.groq.com/openai/v1",
# )

# print("✅ Groq loaded")

# app = FastAPI()

# class ChatRequest(BaseModel):
#     messages: list

# @app.post("/api/chat")
# def chat(req: ChatRequest):
#     response = client.chat.completions.create(
#         model="openai/gpt-oss-20b", 
#         messages=req.messages
#     )
#     return {"reply": response.choices[0].message.content}



from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path
import os
from openai import OpenAI
from agent import run_agent

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY missing in .env")

client = OpenAI(api_key=api_key)

print("✅ OpenAI loaded")

app = FastAPI()

class ChatRequest(BaseModel):
    messages: list

@app.post("/api/chat")
def chat(req: ChatRequest):
    # last user message
    user_msg = req.messages[-1]["content"]

    reply = run_agent(user_msg)

    return {"reply": reply}