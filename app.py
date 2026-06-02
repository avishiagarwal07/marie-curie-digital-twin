import streamlit as st
from src.agent import create_agent, get_response

# Page config
st.set_page_config(
    page_title="Marie Curie Digital Twin",
    page_icon="⚗️",
    layout="centered"
)

# Header
st.title("⚗️ Marie Curie — Digital Twin")
st.markdown("""
*You are speaking with a digital reconstruction of Marie Curie — 
physicist, chemist, and two-time Nobel laureate. Ask her anything 
about her life, discoveries, and scientific work.*
""")
st.divider()

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "retriever" not in st.session_state:
    with st.spinner("Initializing Marie Curie's knowledge base..."):
        st.session_state.retriever = create_agent()

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    else:
        with st.chat_message("assistant", avatar="⚗️"):
            st.write(message["content"])

# Chat input
if prompt := st.chat_input("Ask Marie Curie anything..."):
    # Add user message to history and display it
    st.session_state.chat_history.append({
        "role": "user",
        "content": prompt
    })
    with st.chat_message("user"):
        st.write(prompt)

    # Get and display Marie Curie's response
    with st.chat_message("assistant", avatar="⚗️"):
        with st.spinner("Marie Curie is thinking..."):
            response = get_response(
                prompt,
                st.session_state.chat_history[:-1],
                st.session_state.retriever
            )
        st.write(response)

    # Add response to history
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response
    })