from langfuse import Langfuse
from app.core.config import get_settings
import os

settings = get_settings()

# Initialize Langfuse client
langfuse = None

try:
    secret_key = settings.LANGFUSE_SECRET_KEY or os.getenv("LANGFUSE_SECRET_KEY")
    public_key = settings.LANGFUSE_PUBLIC_KEY or os.getenv("LANGFUSE_PUBLIC_KEY")
    host = settings.LANGFUSE_HOST or os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
    
    if secret_key and public_key:
        langfuse = Langfuse(
            secret_key=secret_key,
            public_key=public_key,
            host=host
        )
        print("=" * 50)
        print("✅ Langfuse initialized successfully")
        print(f"   Host: {host}")
        print("=" * 50)
    else:
        print("⚠️ Langfuse keys not found")
except Exception as e:
    print(f"❌ Failed to initialize Langfuse: {e}")
    langfuse = None

def get_langfuse():
    return langfuse
