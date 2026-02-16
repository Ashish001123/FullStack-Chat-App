import os
from dotenv import load_dotenv
from app_knowledge import APP_KNOWLEDGE
from openai import OpenAI
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if client:
    print("OpenAI API key loaded successfully.")
else:
    print("Failed to load OpenAI API key.")

def run_agent(question: str):

    system = f"""
You are AI assistant for Chatty chat app.
Answer user questions about the app.

App info:
{APP_KNOWLEDGE}
"""

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": question},
        ],
    )

    return resp.choices[0].message.content