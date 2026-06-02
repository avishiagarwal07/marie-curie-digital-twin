import streamlit as st
from src.agent import create_agent, get_response
from src.memory import load_long_term_memory

st.set_page_config(
    page_title="Marie Curie Digital Twin",
    page_icon="⚗️",
    layout="wide"
)

st.markdown("""
<style>
    /* Overall background */
    .stApp {
        background-color: #f0efed;
    }

    /* Sidebar panel background */
    section[data-testid="stSidebar"] {
        background-color: #e8e6e3;
        border-right: 1px solid #d4d1cd;
    }

    /* Chat messages */
    .stChatMessage {
        background-color: #ffffff;
        border-radius: 6px;
        border: 1px solid #e0dedd;
    }

    /* Input box */
    .stChatInput input {
        background-color: #ffffff;
        border: 1px solid #ccc;
        border-radius: 6px;
    }
    /* User message background */
    [data-testid="stChatMessage"] {
            background-color: #e8e6e3 !important;
            border: none !important;
            border-radius: 8px !important;
    }

    /* Main content area background */
    .main .block-container {
            background-color: #f0efed;
    }

    /* Remove white from chat input area */
    [data-testid="stChatInput"] {
            background-color: #e8e6e3 !important;
            border: 1px solid #ccc !important;
            border-radius: 8px !important;
    }

    /* Text in chat messages */
    [data-testid="stChatMessage"] p {
            color: #2a2a2a;
    }

    /* Memory section headers */
    .mem-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        color: #999;
        margin-bottom: 6px;
    }

    /* Individual memory entry */
    .mem-entry {
        font-size: 13px;
        color: #444;
        padding: 7px 0;
        border-bottom: 1px solid #d8d5d2;
        line-height: 1.4;
    }

    .mem-date {
        font-size: 11px;
        color: #bbb;
        margin-top: 2px;
    }

    /* Stat boxes */
    .stat-box {
        background-color: #dedad6;
        border-radius: 6px;
        padding: 12px;
        text-align: center;
        margin-bottom: 8px;
    }

    .stat-num {
        font-size: 26px;
        font-weight: 700;
        color: #2a2a2a;
    }

    .stat-lbl {
        font-size: 11px;
        color: #777;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    /* Title area */
    .title-block {
        padding: 8px 0 4px 0;
    }

    .title-name {
        font-size: 26px;
        font-weight: 700;
        color: #1a1a1a;
        letter-spacing: -0.3px;
    }

    .title-sub {
        font-size: 13px;
        color: #888;
        margin-top: 2px;
    }

    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #d4d1cd;
        margin: 12px 0;
    }

    /* Clear button */
    .stButton button {
        background-color: #dedad6;
        color: #444;
        border: 1px solid #ccc;
        border-radius: 5px;
        font-size: 13px;
        width: 100%;
    }

    .stButton button:hover {
        background-color: #d0ccc8;
        color: #222;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "retriever" not in st.session_state:
    with st.spinner("Loading..."):
        st.session_state.retriever = create_agent()

# Left sidebar — memory panel
with st.sidebar:
    st.markdown('<div class="title-name">Memory</div>', unsafe_allow_html=True)
    st.markdown('<div class="title-sub">What Marie Curie remembers</div>', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    memory = load_long_term_memory()
    conversations = memory.get("conversations", [])

    # Stats row
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'<div class="stat-box">'
            f'<div class="stat-num">{len(conversations)}</div>'
            f'<div class="stat-lbl">Exchanges</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    with col2:
        sessions = len(set(c["timestamp"][:10] for c in conversations)) if conversations else 0
        st.markdown(
            f'<div class="stat-box">'
            f'<div class="stat-num">{sessions}</div>'
            f'<div class="stat-lbl">Sessions</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Recent topics
    st.markdown('<div class="mem-label">Recent Topics</div>', unsafe_allow_html=True)

    if conversations:
        for exchange in reversed(conversations[-8:]):
            question = exchange["user"]
            if len(question) > 55:
                question = question[:55] + "..."
            date = exchange["timestamp"][:10]
            st.markdown(
                f'<div class="mem-entry">{question}'
                f'<div class="mem-date">{date}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            '<div style="font-size:13px; color:#aaa; padding: 8px 0;">No conversations yet.</div>',
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Clear Memory"):
        import os
        if os.path.exists("data/memory.json"):
            os.remove("data/memory.json")
        st.session_state.chat_history = []
        st.rerun()

# Main chat area
st.markdown(
    '<div class="title-block">'
    '<div class="title-name">Marie Curie</div>'
    '<div class="title-sub">Physicist · Chemist · Nobel Laureate · 1867 — 1934</div>'
    '</div>',
    unsafe_allow_html=True
)
st.markdown("<hr>", unsafe_allow_html=True)

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    else:
        with st.chat_message("assistant"):
            st.write(message["content"])

# Chat input
if prompt := st.chat_input("Ask Marie Curie anything..."):
    st.session_state.chat_history.append({
        "role": "user",
        "content": prompt
    })
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner(""):
            response = get_response(
                prompt,
                st.session_state.chat_history[:-1],
                st.session_state.retriever
            )
        st.write(response)

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response
    })
    st.rerun()