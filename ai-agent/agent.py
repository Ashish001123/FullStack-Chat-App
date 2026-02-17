import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from app_knowledge import APP_KNOWLEDGE

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY missing")

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)
print("✅ OpenAI key loaded")

def run_agent(question: str):
    system = f"""
    You are the AI assistant for the Chatty chat application.

    Your job:
    - Answer ONLY questions about the Chatty app
    - Features
    - Usage
    - Accounts
    - Messages
    - Settings
    - Technical help related to the app

    STRICT RULE:
    If the user asks ANYTHING unrelated to the Chatty app,
    you MUST refuse politely.

    Refusal format:
    "Sorry, I can only help with questions about the Chatty app."

    App knowledge:
    {APP_KNOWLEDGE}
    """
    resp = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": question},
        ],
    )
    return resp.choices[0].message.content