from dotenv import load_dotenv
from openai import OpenAI
from rag.rag import retrieve
from mem0 import Memory
import uuid


load_dotenv()

client = OpenAI()

config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333
        }
    }
}

memory_client = Memory.from_config(config)

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
- Make answers visually clean and chat-friendly

- Keep answers short, clear, and helpful
- Use friendly tone with emojis 😊
"""

def get_safe_user_id(user_id):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, user_id))

def run_agent(user_query: str, user_id: str):
    print("USER ID:", user_id)
    try:
        
        safe_user_id = get_safe_user_id(user_id)

        context_chunks = retrieve(user_query)

        if not context_chunks:
            context_chunks = retrieve("chatty application features messaging flow authentication")
        context = "\n\n".join(context_chunks) if isinstance(context_chunks, list) else context_chunks

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
            ]
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


