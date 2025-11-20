from rag.document_processor import DocumentProcessor
from rag.vector_store import get_vector_store

# Test text
sample_text = """
Tesla Inc. reported Q4 2024 revenue of $25.2 billion, up 8% year-over-year.
The company delivered 484,507 vehicles in Q4, meeting analyst expectations.
Gross margin was 17.2%, slightly below the previous quarter's 17.9%.
Operating income reached $2.1 billion with a 8.2% operating margin.
"""

print("🔄 Processing document...")
processor = DocumentProcessor(chunk_size=200, chunk_overlap=50)
chunks = processor.process_text(sample_text, source="Tesla Q4 2024 Report")
print(f"✅ Created {len(chunks)} chunks")

print("\n🔄 Initializing vector store...")
vector_store = get_vector_store(collection_name="test_collection")

print("\n🔄 Adding documents to vector store...")
vector_store.add_documents(chunks)
print("✅ Documents added!")

print("\n🔍 Testing retrieval...")
query = "What was Tesla's revenue in Q4?"
results = vector_store.similarity_search(query, k=2)

print(f"\n📊 Query: '{query}'")
print(f"Found {len(results)} relevant chunks:\n")
for i, doc in enumerate(results, 1):
    print(f"Chunk {i}:")
    print(doc.page_content)
    print(f"Source: {doc.metadata['source']}\n")

print("✅ RAG Pipeline Test Complete!")
