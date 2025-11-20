from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from app.core.config import get_settings
from app.rag.vector_store import get_vector_store

settings = get_settings()

class SummaryAgent:
    """Agent specialized in creating summaries and executive briefs."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.vector_store = get_vector_store()
        
        self.prompt = ChatPromptTemplate.from_template("""
You are an executive summary specialist. Create clear, concise summaries.

Content to summarize:
{context}

Task: {question}

Instructions:
1. Identify the most important information
2. Create a structured summary with key points
3. Use bullet points for clarity
4. Keep it concise but comprehensive
5. Highlight key metrics and insights

Summary:""")
        
        self.chain = (
            {"context": self._get_context, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
    
    def _get_context(self, question: str) -> str:
        """Retrieve relevant content from vector store."""
        docs = self.vector_store.similarity_search(question, k=5)
        return "\n\n".join([doc.page_content for doc in docs])
    
    def summarize(self, question: str) -> str:
        """Create a summary based on the question."""
        return self.chain.invoke(question)
