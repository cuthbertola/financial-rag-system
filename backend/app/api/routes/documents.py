from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db, Document
from app.models.schemas import DocumentUploadResponse, DocumentInfo
from app.rag.document_processor import DocumentProcessor
from app.rag.vector_store import get_vector_store

router = APIRouter(prefix="/documents", tags=["documents"])
processor = DocumentProcessor()
vector_store = get_vector_store()

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload and process a document."""
    try:
        # Read file content
        content = await file.read()
        
        # Process document based on file type
        if file.filename.endswith('.pdf'):
            chunks = processor.process_pdf(content, file.filename)
            file_type = "pdf"
        elif file.filename.endswith('.txt'):
            text = content.decode('utf-8')
            chunks = processor.process_text(text, file.filename)
            file_type = "text"
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Use PDF or TXT.")
        
        # Add to vector store
        vector_store.add_documents(chunks)
        
        # Save to database
        db_doc = Document(
            filename=file.filename,
            file_type=file_type,
            content_preview=chunks[0].page_content[:200] if chunks else "",
            num_chunks=len(chunks)
        )
        db.add(db_doc)
        db.commit()
        db.refresh(db_doc)
        
        return DocumentUploadResponse(
            id=db_doc.id,
            filename=db_doc.filename,
            file_type=db_doc.file_type,
            num_chunks=db_doc.num_chunks,
            message=f"Successfully processed {len(chunks)} chunks"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list", response_model=list[DocumentInfo])
async def list_documents(db: Session = Depends(get_db)):
    """List all uploaded documents."""
    documents = db.query(Document).order_by(Document.uploaded_at.desc()).all()
    return documents

@router.delete("/{document_id}")
async def delete_document(document_id: int, db: Session = Depends(get_db)):
    """Delete a document."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    db.delete(doc)
    db.commit()
    return {"message": f"Document {doc.filename} deleted successfully"}
