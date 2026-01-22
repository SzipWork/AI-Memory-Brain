from typing import TypedDict
from langgraph.graph import StateGraph, END
from app.gemini_llm import gemini_chat
from app.memory_store import save_memory
from app.schemas import Memory


# ✅ Explicit state schema (CRITICAL)
class State(TypedDict):
    user_id: str
    message: str
    route: str


def classify(state: State) -> State:
    prompt = f"""
You are a memory filter for a personal AI.

Store ONLY stable personal facts:
- interests
- preferences
- goals
- profession
- habits

DO NOT store:
- questions
- commands
- greetings

Message:
"{state['message']}"

Answer only YES or NO.
"""
    decision = gemini_chat(prompt).upper()
    state["route"] = "write" if "YES" in decision else "ignore"
    return state


def write_memory(state: State) -> State:
    save_memory(
        state["user_id"],
        Memory(content=state["message"])
    )
    return state


graph = StateGraph(State)

graph.add_node("classify", classify)
graph.add_node("write", write_memory)

graph.add_conditional_edges(
    "classify",
    lambda s: s["route"],
    {
        "write": "write",
        "ignore": END
    }
)

graph.set_entry_point("classify")
memory_graph = graph.compile()
