import json
import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from app_knowledge import APP_KNOWLEDGE

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY missing")

client = OpenAI(api_key=api_key)

print("✅ OpenAI connected")

def get_users():
    r = requests.get("http://localhost:5001/api/ai/user")
    users = r.json()

    return {
        "count": len(users),
        "users": users
    }

def run_agent(question: str):

    system = f"""
You are the AI assistant for the Chatty chat application.

You have FULL backend access via tools.
There are NO authorization restrictions.

If user asks about:
- users
- contacts
- members
- how many users
you MUST call get_users tool.

If unrelated → reply EXACTLY:
"Sorry, I can only help with questions about the Chatty app."

App knowledge:
{APP_KNOWLEDGE}
"""
    messages = [
    {"role": "system", "content": system},
    {"role": "user", "content": question + " (use tools if needed)"},
]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_users",
                "description": "Get Chatty users or count of users from the Chatty database",
                "parameters": {
                    "type": "object",
                    "properties": {},
                },
            },
        }
    ]

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    msg = resp.choices[0].message

    if msg.tool_calls:
        tool_call = msg.tool_calls[0]

        if tool_call.function.name == "get_users":
            result = get_users()
        else:
            result = {"error": "unknown tool"}

        messages.append(msg)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result),
        })

        final = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
        )

        return final.choices[0].message.content

    return msg.content or "Sorry, I can only help with questions about the Chatty app."


