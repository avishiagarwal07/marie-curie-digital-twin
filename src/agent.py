import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from src.persona import get_persona
from src.retriever import load_retriever, retrieve_context
from src.memory import (
    load_long_term_memory,
    add_to_long_term_memory,
    get_conversation_history
)

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def create_agent():
    retriever = load_retriever()
    return retriever

def get_response(user_message: str, chat_history: list, retriever) -> str:
    # Step 1: Retrieve relevant chunks from ChromaDB
    context = retrieve_context(user_message, retriever)

    # Step 2: Load long term memory
    long_term_memory = load_long_term_memory()
    history_text = get_conversation_history(long_term_memory)

    # Step 3: Build the full prompt
    persona = get_persona()

    full_prompt = f"""
## Relevant Knowledge from Your Research and Work:
{context}

## Previous Conversation History:
{history_text}

## Current Question:
{user_message}

Remember: You are Marie Curie. Respond in first person, 
in character, using the knowledge provided above.
"""

    # Step 4: Build chat history for Gemini
    gemini_history = []
    for message in chat_history:
        role = "user" if message["role"] == "user" else "model"
        gemini_history.append(
            types.Content(
                role=role,
                parts=[types.Part(text=message["content"])]
            )
        )

    # Step 5: Send to Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=persona,
        ),
        contents=gemini_history + [
            types.Content(
                role="user",
                parts=[types.Part(text=full_prompt)]
            )
        ]
    )

    assistant_message = response.text

    # Step 6: Save to long term memory
    add_to_long_term_memory(user_message, assistant_message)

    return assistant_message