# ChromaDB - Querying the Database
# This script demonstrates how to query the persistent ChromaDB collection using a user query. It   converts the query into an embedding using Ollama, retrieves similar records from ChromaDB, and then uses a language model to summarize the retrieved context.
# Flow is User Query -> Embedding Generation -> Retrieve from ChromaDB -> Summarize with LLM
import chromadb
import ollama

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("pdf_docs")

query = "What is Data and its type?"

# Create embedding for query
embedding = ollama.embed(
    model="nomic-embed-text:latest",
    input=query
)["embeddings"][0]

# Retrieve relevant chunks
results = collection.query(
    query_embeddings=[embedding],
    n_results=2
)

docs = results["documents"][0]

# Combine chunks into context
context = "\n\n".join(docs)

# Send to LLM
prompt = f"""
You are a QA system.

Rules:
- Answer ONLY using the provided context.
- If the answer is not present, reply EXACTLY:
  "Answer not found in provided documents."
Context:
  {context}

Question: {query}
"""

response = ollama.chat(
    model="llama3",
    messages=[{"role": "user", "content": prompt}]
)

print(response["message"]["content"])
