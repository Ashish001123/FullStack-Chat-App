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
    allow_origins=[
    "http://localhost:5173",
    "https://fullstack-chat-app-32t0.onrender.com"
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Query(BaseModel):
    message : str
    userId : str

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
            user_id=query.userId  
        )
        return {
            "result": response 
        }
    except Exception as e:
        print("ERROR:", e) 
        import traceback
        traceback.print_exc()
        return {"error": str(e)}
        

    