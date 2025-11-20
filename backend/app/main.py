from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import documents, chat, metrics
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="Financial RAG System",
    description="Multi-Agent RAG System for Financial Analysis",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(documents.router)
app.include_router(chat.router)
app.include_router(metrics.router)

@app.get("/")
async def root():
    return {
        "message": "Financial RAG System API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
