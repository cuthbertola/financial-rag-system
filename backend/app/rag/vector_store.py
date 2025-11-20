import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_community.vectorstores import Chroma
from app.core.config import get_settings
from app.rag.embeddings import get_embeddings

settings = get_settings()

def get_vector_store(collection_name: str = "financial_docs"):
    """Initialize ChromaDB vector store."""
    embeddings = get_embeddings()
    
    client = chromadb.Client(ChromaSettings(
        persist_directory=settings.CHROMA_PERSIST_DIR,
        anonymized_telemetry=False
    ))
    
    vector_store = Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=embeddings
    )
    
    return vector_store
