from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DocumentUploadResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    num_chunks: int
    message: str

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    session_id: str
    sources: list[str] = []

class DocumentInfo(BaseModel):
    id: int
    filename: str
    file_type: str
    num_chunks: int
    uploaded_at: datetime
    
    class Config:
        from_attributes = True
