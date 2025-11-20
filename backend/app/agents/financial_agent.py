from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from app.core.config import get_settings
from app.rag.vector_store import get_vector_store

settings = get_settings()

class FinancialAgent:
    """Agent specialized in financial calculations and analysis."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.vector_store = get_vector_store()
        
        self.prompt = ChatPromptTemplate.from_template("""
You are a financial analyst specializing in calculations and financial metrics.

Use the following financial data to perform analysis:

Context:
{context}

Task: {question}

Instructions:
1. Extract relevant financial numbers from the context
2. Perform any necessary calculations
3. Compute financial ratios or metrics if applicable
4. Provide clear numerical answers with units
5. Show your calculation steps if performing computations

Answer:""")
        
        self.chain = (
            {"context": self._get_context, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
    
    def _get_context(self, question: str) -> str:
        """Retrieve relevant financial data from vector store."""
        docs = self.vector_store.similarity_search(question, k=3)
        return "\n\n".join([doc.page_content for doc in docs])
    
    def analyze(self, question: str) -> str:
        """Perform financial analysis based on the question."""
        return self.chain.invoke(question)
