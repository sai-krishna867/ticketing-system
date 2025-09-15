import streamlit as st
from core.runner import run_graph
from agents.response_agent import generate_response

st.set_page_config(page_title="AI Ticketing System", page_icon="🎫", layout="wide")
st.title("🎫 AI-Powered Ticketing System")

# Session history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
if prompt := st.chat_input(""👋 Hi! I’m your AI Ticket Assistant. Tell me your issue, and I’ll create or check a JIRA ticket for you."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Run pipeline
    final_state = run_graph(prompt)

    # Generate AI response
    reply = generate_response(final_state.__dict__)

    # Show assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
