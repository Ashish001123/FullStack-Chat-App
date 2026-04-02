# from dotenv import load_dotenv
# from openai import OpenAI
# from rag.rag import retrieve
# from mem0 import Memory
# import uuid


# load_dotenv()

# client = OpenAI()

# config = {
#     "vector_store": {
#         "provider": "qdrant",
#         "config": {
#             "host": "localhost",
#             "port": 6333
#         }
#     }
# }

# memory_client = Memory.from_config(config)

# SYSTEM_PROMPT = """
# You are an AI assistant for the Chatty application.

# STRICT RULES:
# - First check Past Memory for personal questions (like name, preferences, etc.)
# - Acknowledge when the user shares personal facts, introduces themselves, or greets you.
# - Answer app questions from provided context (RAG)
# - Do NOT use your own knowledge for external facts.
# - If the user asks a question out of scope or not found in context/memory, say:
#   "I can only help with the chatty application information 😊"

# FORMATTING RULES:
# - DO NOT use markdown (#, ##, ###)
# - Use emojis instead for headings
# - Use bullet points and spacing for clean UI
# - Make answers visually clean and chat-friendly

# - Keep answers short, clear, and helpful
# - Use friendly tone with emojis 😊
# """

# def get_safe_user_id(user_id):
#     return str(uuid.uuid5(uuid.NAMESPACE_DNS, user_id))

# def run_agent(user_query: str, user_id: str):
#     print("USER ID:", user_id)
#     try:
        
#         safe_user_id = get_safe_user_id(user_id)

#         context_chunks = retrieve(user_query)

#         if not context_chunks:
#             context_chunks = retrieve("chatty application features messaging flow authentication")
#         context = "\n\n".join(context_chunks) if isinstance(context_chunks, list) else context_chunks

#         try:
#             memories = memory_client.search(query=user_query, user_id=safe_user_id)
#         except Exception:
#             try:
#                 memories = memory_client.get_all(user_id=safe_user_id)
#             except Exception:
#                 memories = {}

#         if isinstance(memories, dict) and "results" in memories:
#             memories_list = memories["results"]
#         else:
#             memories_list = memories if isinstance(memories, list) else []

#         past_memory = "\n".join(
#             [m.get("memory", m.get("text", "")) if isinstance(m, dict) else str(m) for m in memories_list]
#         ) if memories_list else ""

#         prompt = f"""
# Context:
# {context}

# Past Memory:
# {past_memory}

# Question:
# {user_query}
# """

#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": SYSTEM_PROMPT},
#                 {"role": "user", "content": prompt}
#             ]
#         )

#         reply = response.choices[0].message.content

#         memory_client.add(
#             user_id=safe_user_id,
#             messages=[
#                 {"role": "user", "content": user_query},
#                 {"role": "assistant", "content": reply}
#             ]
#         )

#         return reply

#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         return "AI error"




from dotenv import load_dotenv
from openai import OpenAI
from rag.rag import retrieve
from mem0 import Memory
import uuid
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333
        }
    }
}

# memory_client = Memory.from_config(config)
memory_client = None
SYSTEM_PROMPT = """
You are an AI assistant for the Chatty application.

STRICT RULES:
- First check Past Memory for personal questions (like name, preferences, etc.)
- Acknowledge when the user shares personal facts, introduces themselves, or greets you.
- Answer app questions from provided context (RAG)
- Do NOT use your own knowledge for external facts.
- If the user asks a question out of scope or not found in context/memory, say:
  "I can only help with the chatty application information 😊"

FORMATTING RULES:
- DO NOT use markdown (#, ##, ###)
- Use emojis instead for headings
- Use bullet points and spacing for clean UI
- Keep answers short, clear, and helpful
- Use friendly tone with emojis 😊
"""

def get_safe_user_id(user_id):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, user_id))

def improve_text(user_text: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an English assistant. "
                        "Fix grammar, improve clarity, make it natural. "
                        "Add relevant emojis. Keep it short and friendly."
                        "Always give user 4 to 5 sentence of better english in seperated line and formated manner"
                    )
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ],
            max_tokens=150,
            temperature=0.7
        )

        improved = response.choices[0].message.content.strip()

        return f"✍️ Improved Text:\n{improved}"

    except Exception as e:
        return f"Error: {str(e)}"


def detect_intent(user_query: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Classify the intent as either 'improve_text' or 'chat_query'. Only return one word."
                },
                {
                    "role": "user",
                    "content": user_query
                }
            ],
            max_tokens=5
        )

        return response.choices[0].message.content.lower()

    except:
        return "chat_query"



def run_agent(user_query: str, user_id: str):
    print("USER ID:", user_id)

    try:
        safe_user_id = get_safe_user_id(user_id)

        intent = detect_intent(user_query)
        if "improve" in intent or any(word in user_query.lower() for word in ["correct", "fix", "grammar", "rewrite"]):
            return improve_text(user_query)

        context_chunks = retrieve(user_query)

        if not context_chunks:
            context_chunks = retrieve("chatty application features messaging flow authentication")

        context = "\n\n".join(context_chunks) if isinstance(context_chunks, list) else context_chunks

        # try:
        #     memories = memory_client.search(query=user_query, user_id=safe_user_id)
        # except Exception:
        #     try:
        #         memories = memory_client.get_all(user_id=safe_user_id)
        #     except Exception:
        #         memories = {}
        try:
            memories = memory_client.search(query=user_query, user_id=safe_user_id)
        except Exception:
            try:
                memories = memory_client.get_all(user_id=safe_user_id)
            except Exception:
                memories = {}

        if isinstance(memories, dict) and "results" in memories:
            memories_list = memories["results"]
        else:
            memories_list = memories if isinstance(memories, list) else []

        past_memory = "\n".join(
            [m.get("memory", m.get("text", "")) if isinstance(m, dict) else str(m) for m in memories_list]
        ) if memories_list else ""

        prompt = f"""
Context:
{context}

Past Memory:
{past_memory}

Question:
{user_query}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        reply = response.choices[0].message.content


        memory_client.add(
            user_id=safe_user_id,
            messages=[
                {"role": "user", "content": user_query},
                {"role": "assistant", "content": reply}
            ]
        )

        return reply

    except Exception as e:
        import traceback
        traceback.print_exc()
        return "AI error"
