from agents.research_agent import ResearchAgent
from rag.document_processor import DocumentProcessor
from rag.vector_store import get_vector_store

# Sample financial document
sample_text = """
Tesla Inc. reported Q4 2024 revenue of $25.2 billion, up 8% year-over-year.
The company delivered 484,507 vehicles in Q4, meeting analyst expectations.
Gross margin was 17.2%, slightly below the previous quarter's 17.9%.
Operating income reached $2.1 billion with a 8.2% operating margin.
Free cash flow was $2.3 billion for the quarter.
"""

print("📄 Adding document to knowledge base...")
processor = DocumentProcessor(chunk_size=200, chunk_overlap=50)
chunks = processor.process_text(sample_text, source="Tesla Q4 2024 Report")
vector_store = get_vector_store(collection_name="financial_docs")
vector_store.add_documents(chunks)
print(f"✅ Added {len(chunks)} chunks to knowledge base\n")

print("🤖 Initializing Research Agent...")
agent = ResearchAgent()
print("✅ Agent ready!\n")

questions = [
    "What was Tesla's Q4 2024 revenue?",
    "How many vehicles did Tesla deliver in Q4?",
    "What was the operating margin?",
    "What was the free cash flow?"
]

for q in questions:
    print(f"❓ {q}")
    answer = agent.ask(q)
    print(f"💡 {answer}\n")

print("✅ Agent Test Complete!")
