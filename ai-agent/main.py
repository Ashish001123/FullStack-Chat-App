# from fastapi import FastAPI
# from pydantic import BaseModel
# from dotenv import load_dotenv
# from pathlib import Path
# import os
# from openai import OpenAI
# from agent import run_agent

# env_path = Path(__file__).parent / ".env"
# load_dotenv(dotenv_path=env_path)

# api_key = os.getenv("OPENAI_API_KEY")

# if not api_key:
#     raise ValueError("❌ OPENAI_API_KEY missing in .env")

# client = OpenAI(api_key=api_key)

# print("✅ OpenAI loaded")

# app = FastAPI()

# class ChatRequest(BaseModel):
#     messages: list
#     userId: str

# @app.post("/api/chat")
# def chat(req: ChatRequest):
#     user_msg = req.messages[-1]["content"]

#     reply = run_agent(user_msg, req.userId)

#     return {"reply": reply}



from pydantic import BaseModel
from fastapi import FastAPI
from openai import OpenAI
from dotenv import load_dotenv
from agent import run_agent
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

client = OpenAI()
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # ✅ correct
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Query(BaseModel):
    message : str


@app.get("/")

def home():
    return {"api is running"}

@app.get("/")
def home():
    return {"message": "AI is running 🚀"}

@app.post("/chat")
def chat(query: Query):
    try:
        response = run_agent(
            user_query=query.message,
        )
        return {
            "result": response 
        }
    except Exception as e:
        print("ERROR:", e) 
        return {"error": str(e)}
        

    