from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from pypdf import PdfReader
import io

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
    
    def process_pdf(self, file_content: bytes, filename: str) -> List[Document]:
        """Extract text from PDF and split into chunks."""
        pdf_file = io.BytesIO(file_content)
        pdf_reader = PdfReader(pdf_file)
        
        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        # Create document with metadata
        doc = Document(
            page_content=text,
            metadata={"source": filename, "type": "pdf"}
        )
        
        # Split into chunks
        chunks = self.text_splitter.split_documents([doc])
        return chunks
    
    def process_text(self, text: str, source: str = "text") -> List[Document]:
        """Process plain text and split into chunks."""
        doc = Document(
            page_content=text,
            metadata={"source": source, "type": "text"}
        )
        
        chunks = self.text_splitter.split_documents([doc])
        return chunks
