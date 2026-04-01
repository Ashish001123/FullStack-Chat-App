# import json
# import os
# import requests
# from pathlib import Path
# from dotenv import load_dotenv
# from openai import OpenAI
# from app_knowledge import APP_KNOWLEDGE

# env_path = Path(__file__).parent / ".env"
# load_dotenv(dotenv_path=env_path)

# api_key = os.getenv("OPENAI_API_KEY")
# if not api_key:
#     raise ValueError("OPENAI_API_KEY missing")

# client = OpenAI(api_key=api_key)

# BASE_URL = "http://localhost:5001/api/ai"


# # ------------------ API CALLS ------------------

# def get_users():
#     try:
#         r = requests.get(f"{BASE_URL}/user", timeout=5)
#         return r.json()
#     except Exception as e:
#         return {"error": str(e)}


# def search_user(name: str):
#     try:
#         r = requests.get(
#             f"{BASE_URL}/search",
#             params={"q": name},
#             timeout=5,
#         )
#         return r.json()
#     except Exception as e:
#         return {"error": str(e)}


# def send_message(to_user_id: str, text: str, from_user_id: str):
#     try:
#         r = requests.post(
#             f"{BASE_URL}/send",
#             json={
#                 "toUserId": to_user_id,
#                 "text": text,
#                 "fromUserId": from_user_id,
#             },
#             timeout=5,
#         )
#         return r.json()
#     except Exception as e:
#         return {"error": str(e)}


# # ------------------ AGENT ------------------

# def run_agent(question: str, current_user_id: str):

#     system_prompt = f"""
# You are the AI assistant for the Chatty chat application.

# You can:
# - list users
# - search users by name
# - send messages to users
# - help with chat features

# RULES:
# - If user wants to send a message → ALWAYS search user first
# - Use ONLY the _id returned from search
# - NEVER invent userIds
# - If user not found → say politely

# App knowledge:
# {APP_KNOWLEDGE}
# """

#     messages = [
#         {"role": "system", "content": system_prompt},
#         {"role": "user", "content": question},
#     ]

#     tools = [
#         {
#             "type": "function",
#             "function": {
#                 "name": "get_users",
#                 "description": "Get all Chatty users",
#                 "parameters": {"type": "object", "properties": {}},
#             },
#         },
#         {
#             "type": "function",
#             "function": {
#                 "name": "search_user",
#                 "description": "Search a Chatty user by name",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {"name": {"type": "string"}},
#                     "required": ["name"],
#                 },
#             },
#         },
#         {
#             "type": "function",
#             "function": {
#                 "name": "send_message",
#                 "description": "Send a message to a userId",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "to_user_id": {"type": "string"},
#                         "text": {"type": "string"},
#                     },
#                     "required": ["to_user_id", "text"],
#                 },
#             },
#         },
#     ]

#     resp = client.chat.completions.create(
#         model="gpt-4.1-mini",
#         messages=messages,
#         tools=tools,
#         tool_choice="auto",
#     )

#     msg = resp.choices[0].message

#     # ------------------ TOOL HANDLING ------------------

#     if msg.tool_calls:
#         for tool_call in msg.tool_calls:
#             name = tool_call.function.name
#             args = json.loads(tool_call.function.arguments or "{}")

#             # ---------- GET USERS ----------
#             if name == "get_users":
#                 result = get_users()

#             # ---------- SEARCH USER ----------
#             elif name == "search_user":
#                 users = search_user(args.get("name"))

#                 if not users:
#                     result = {"error": "User not found"}
#                 else:
#                     # return ONLY Mongo id
#                     result = {
#                         "userId": users[0]["_id"],
#                         "fullName": users[0]["fullName"],
#                     }

#             # ---------- SEND MESSAGE ----------
#             elif name == "send_message":
#                 to_user_id = args.get("to_user_id")
#                 text = args.get("text")

#                 if not to_user_id or len(to_user_id) < 10:
#                     result = {"error": "Invalid userId"}
#                 else:
#                     api_result = send_message(
#                         to_user_id,
#                         text,
#                         current_user_id,
#                     )

#                     result = {
#                         "status": "sent",
#                         "toUserId": to_user_id,
#                         "text": text,
#                         "api": api_result,
#                     }

#             else:
#                 result = {"error": "unknown tool"}

#             # append tool result
#             messages.append(msg)
#             messages.append({
#                 "role": "tool",
#                 "tool_call_id": tool_call.id,
#                 "content": json.dumps(result),
#             })

#         # final assistant response
#         final = client.chat.completions.create(
#             model="gpt-4.1-mini",
#             messages=messages,
#         )

#         return final.choices[0].message.content

#     return msg.content




from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI()

SYSTEM_PROMPT="""
    You are an perfect chat assistant for this chatty application. 
    
"""

def run_agent(user_query):
    try:
        message_history = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=message_history
        )

        reply = response.choices[0].message.content
        return reply

    except Exception as e:
        print("OPENAI ERROR:", e)   # 👈 IMPORTANT
        return "Error connecting to AI"