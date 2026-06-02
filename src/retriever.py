from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

VECTOR_STORE_PATH = "data/processed/chroma_db"

def load_retriever():
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    vector_store = Chroma(
        persist_directory=VECTOR_STORE_PATH,
        embedding_function=embeddings
    )
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 6,
            "fetch_k": 20
        }
    )
    return retriever

def retrieve_context(query, retriever):
    docs = retriever.invoke(query)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    return context, docs

if __name__ == "__main__":
    print("Loading retriever...")
    retriever = load_retriever()
    
    test_query = "What did Marie Curie discover?"
    print(f"\nQuery: {test_query}")
    print("\nRetrieved context:")
    print(retrieve_context(test_query, retriever))