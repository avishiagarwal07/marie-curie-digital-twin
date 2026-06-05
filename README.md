# Marie Curie Digital Twin

A timeline-aware digital twin of Marie Curie built using Retrieval-Augmented Generation (RAG), Gemini, and persistent memory.

The system allows users to have conversations with Marie Curie while staying grounded in historical documents, her scientific work, and the specific period of her life selected by the user.

## Features

- RAG pipeline using Marie Curie's writings, Nobel lectures, biographies, and historical sources
- First-person Marie Curie persona
- Timeline-aware conversations (1898, 1903, 1911, 1918, 1934)
- Long-term memory across sessions
- Streamlit-based chat interface
- ChromaDB vector database with semantic retrieval

## Tech Stack

- Gemini 2.5 Flash Lite
- LangChain
- HuggingFace `all-MiniLM-L6-v2`
- ChromaDB
- Streamlit
- Python

## System Workflow

1. User submits a query through Streamlit+ chosen timeline.
2. Relevant knowledge is retrieved from ChromaDB.
3. Previous conversations are loaded from memory.
4. Marie Curie's persona+timeline is applied.
5. Gemini generates a response using retrieved knowledge and memory.
6. The response is stored for future interactions.

## Running the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Add your Gemini API key to `.env`:

```env
GEMINI_API_KEY=your_api_key_here
```

Build the vector database:

```bash
python src/ingest.py
```

Run the application:

```bash
streamlit run app.py
```

## Future Improvements
- Hybrid retrieval (BM25 + vector search)
- Source-aware citations
- Improved memory summarization
- Multi-session conversation support

## Author

Avishi Agarwal