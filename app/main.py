from fastapi import FastAPI
from pydantic import BaseModel
from app.memory_router import memory_graph
from app.memory_store import get_memories
from app.gemini_llm import gemini_chat

app = FastAPI()

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    answer: str

RECALL_TRIGGERS = [
    "remember",
    "remind",
    "what do you know",
    "about me",
    "my interests",
    "my goal"
]

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    msg = req.message.lower()

    if any(k in msg for k in RECALL_TRIGGERS):
        memories = get_memories(req.user_id)

        if not memories:
            return {"answer": "I don’t remember anything about you yet."}

        prompt = f"""
You are a personal AI assistant.

Known facts about the user:
{chr(10).join('- ' + m for m in memories)}

Answer the user's question naturally:
"{req.message}"
"""
        return {"answer": gemini_chat(prompt)}

    memory_graph.invoke({
        "user_id": req.user_id,
        "message": req.message
    })

    return {"answer": "Got it. I’ll remember this if it’s important."}
