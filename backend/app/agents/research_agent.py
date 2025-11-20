from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from app.core.config import get_settings
from app.rag.vector_store import get_vector_store

settings = get_settings()

class ResearchAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.vector_store = get_vector_store()
        
        self.prompt = ChatPromptTemplate.from_template("""
You are a financial research assistant. Use the following context to answer the question.
If you don't know the answer based on the context, say so.

Context:
{context}

Question: {question}

Answer:""")
        
        self.chain = (
            {"context": self._get_context, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
    
    def _get_context(self, question: str) -> str:
        """Retrieve relevant context from vector store."""
        docs = self.vector_store.similarity_search(question, k=3)
        return "\n\n".join([doc.page_content for doc in docs])
    
    def ask(self, question: str) -> str:
        """Ask a question and get an answer based on RAG."""
        return self.chain.invoke(question)
