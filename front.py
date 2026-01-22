# front.py
import streamlit as st
import requests

# -------- CONFIG --------
API_URL = "http://backend:8000/chat"  # change if deployed
# ------------------------

st.set_page_config(page_title="Personal AI Memory Chat", layout="centered")
st.title("🧠 Personal AI Memory Chat")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# User ID input
user_id = st.text_input("User ID", value="user_001")

st.divider()

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Type your message...")

if user_input and user_id:
    # Show user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Call FastAPI backend
    try:
        response = requests.post(
            API_URL,
            json={
                "user_id": user_id,
                "message": user_input
            },
            timeout=30
        )

        if response.status_code == 200:
            answer = response.json()["answer"]
        else:
            answer = f"❌ Error {response.status_code}: {response.text}"

    except Exception as e:
        answer = f"⚠️ Backend not reachable: {e}"

    # Show assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message("assistant"):
        st.markdown(answer)

elif user_input and not user_id:
    st.warning("Please enter a user ID first.")
