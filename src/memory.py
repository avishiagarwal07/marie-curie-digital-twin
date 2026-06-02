import json
import os
from datetime import datetime

# Path for long-term memory storage
MEMORY_FILE = "data/memory.json"

def load_long_term_memory():
    """Load persisted memory from disk"""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {"conversations": [], "key_facts_about_user": []}

def save_long_term_memory(memory: dict):
    """Save memory to disk so it persists across sessions"""
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def add_to_long_term_memory(user_message: str, assistant_message: str):
    """Save a conversation exchange to long term memory"""
    memory = load_long_term_memory()
    memory["conversations"].append({
        "timestamp": datetime.now().isoformat(),
        "user": user_message,
        "assistant": assistant_message
    })
    # Keep only last 50 exchanges to avoid memory getting too large
    memory["conversations"] = memory["conversations"][-50:]
    save_long_term_memory(memory)

def get_conversation_history(memory: dict, last_n: int = 10) -> str:
    """Get recent conversation history as formatted string"""
    conversations = memory["conversations"][-last_n:]
    if not conversations:
        return "No previous conversation history."
    
    history = ""
    for exchange in conversations:
        history += f"User: {exchange['user']}\n"
        history += f"Marie Curie: {exchange['assistant']}\n\n"
    return history.strip()

def format_chat_history(chat_history: list) -> list:
    """Format chat history for Gemini API"""
    formatted = []
    for message in chat_history:
        formatted.append({
            "role": message["role"],
            "parts": [{"text": message["content"]}]
        })
    return formatted