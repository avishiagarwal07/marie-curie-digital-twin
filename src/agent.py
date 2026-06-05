import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_exponential
from src.timeline import TIMELINE

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


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=2, min=2, max=20)
)
def call_gemini(persona, gemini_history, full_prompt):

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
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

    return response.text


def get_response(
    user_message: str,
    chat_history: list,
    retriever,
    current_year: int = 1934
) -> str:

    # Step 1: Retrieve relevant chunks from ChromaDB
    context, docs = retrieve_context(user_message, retriever)
    sources = []

    for doc in docs:
        source = doc.metadata.get("source", "Unknown Source")
        sources.append(source)

    sources_text = "\n".join(set(sources))

    # Step 2: Load long term memory
    long_term_memory = load_long_term_memory()
    history_text = get_conversation_history(long_term_memory)

    # Step 3: Build the full prompt
    persona = get_persona()
    timeline_context = TIMELINE[current_year]

    full_prompt = f"""
## CURRENT YEAR
{current_year}

## CURRENT LIFE CONTEXT
{timeline_context}

IMPORTANT:

You are currently living in the year {current_year}.

Anything that has not yet happened by {current_year}
should be treated as part of the future.

Your personal circumstances must match this year.

## Relevant Knowledge from Your Research and Work:
{context}

## Previous Conversation History:
{history_text}

## Current Question:
{user_message}

Remember:

You are Marie Curie.

Speak in first person.

Your knowledge and personal experiences are limited
to what would be true in the year {current_year}.

Do not speak as though future events have already occurred.
IMPORTANT:

When the retrieved context contains information relevant
to the question, prioritize it over your general knowledge.

Base your answer primarily on the retrieved material.

Do not invent scientific details that are not supported
by the retrieved context.

When discussing discoveries, experiments, radioactivity,
chemistry, or physics, explicitly ground your answer in
the provided material.

If the retrieved context is insufficient,
state that clearly rather than guessing.
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

    # Step 5: Send to Gemini with retries
    try:
        assistant_message = call_gemini(
            persona,
            gemini_history,
            full_prompt
        )

    except Exception as e:
        print(f"Gemini Error: {e}")

        assistant_message = (
            "I apologize, but I am experiencing technical difficulties at the moment. "
            "Please try asking your question again in a few moments."
        )

    # Step 6: Save to long term memory
    add_to_long_term_memory(
        user_message,
        assistant_message
    )

    return assistant_message