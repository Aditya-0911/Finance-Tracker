import streamlit as st
from langchain_core.messages import HumanMessage
from models import AgentState
from graph_builder import build_graph
import json

app = build_graph()

st.title("💸 Expense Tracker with LangGraph")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.chat_input("Enter your expense or say 'summarize'...")

if user_input:
    # keep track of conversation
    st.session_state.history.append(HumanMessage(content=user_input))
    state = AgentState(messages=st.session_state.history)
    result = app.invoke(state)

    # update history with AI messages
    st.session_state.history = result["messages"]

    st.session_state.plot_bytes = result.get("plot_bytes", None)

# helper to detect JSON-like strings
def is_json(text):
    try:
        json.loads(text)
        return True
    except:
        return False

# render conversation
for i, msg in enumerate(st.session_state.history):
    role = "user" if msg.type == "human" else "assistant"
    with st.chat_message(role):
        if role == "assistant" and is_json(msg.content):
            continue
        st.markdown(msg.content)

        # Show plot after the last assistant message
        if (
            role == "assistant"
            and st.session_state.get("plot_bytes")
            and i == len(st.session_state.history) - 1
        ):
            st.image(st.session_state.plot_bytes, caption="Spending Breakdown")
