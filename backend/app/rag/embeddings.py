from langchain_openai import OpenAIEmbeddings
from app.core.config import get_settings

settings = get_settings()

def get_embeddings():
    """Get OpenAI embeddings model."""
    return OpenAIEmbeddings(
        openai_api_key=settings.OPENAI_API_KEY,
        model="text-embedding-3-small"
    )
