# Marie Curie Digital Twin

An AI-powered digital twin of Marie Curie built using Retrieval-Augmented Generation (RAG), Long-Term Memory, and Google's Gemini API.

The project enables users to interact with Marie Curie as if she were alive today, answering questions about her life, scientific discoveries, research, and experiences while maintaining a consistent historical persona.

## Features

* Marie Curie persona with first-person responses
* Retrieval-Augmented Generation (RAG)
* Long-term memory across conversations
* Streamlit-based chat interface
* ChromaDB vector database
* Semantic search using sentence embeddings
* Historical knowledge grounding
* Context-aware multi-turn conversations

## Tech Stack

* Python
* Streamlit
* Google Gemini API
* ChromaDB
* LangChain
* HuggingFace Embeddings
* Sentence Transformers

## Project Structure

```text
marie-curie-digital-twin/
│
├── app.py
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── ingest.py
│   ├── retriever.py
│   ├── agent.py
│   ├── memory.py
│   └── persona.py
│
├── memory.json
├── requirements.txt
└── README.md
```

## System Workflow

1. User submits a query through Streamlit.
2. Relevant knowledge is retrieved from ChromaDB.
3. Previous conversations are loaded from memory.
4. Marie Curie's persona is applied.
5. Gemini generates a response using retrieved knowledge and memory.
6. The response is stored for future interactions.

## Running the Project

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key
```

### Build Vector Database

```bash
python src/ingest.py
```

### Launch Application

```bash
streamlit run app.py
```

## Future Improvements

* Source-aware retrieval
* Hybrid search
* Citation support
* Enhanced memory visualization
* Multi-person historical digital twins

## Author

Avishi Agarwal
