from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path

# Get the backend directory (where .env is)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: str = ""
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/financial_rag"
    
    # Vector DB
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    
    # Observability
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_HOST: str = "https://cloud.langfuse.com"
    
    # Application
    SECRET_KEY: str = "dev-secret-key"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = str(BASE_DIR / ".env")
        case_sensitive = True
        extra = "ignore"

@lru_cache()
def get_settings():
    return Settings()
