# ChromaDB - Querying the Database
# This script demonstrates how to query the persistent ChromaDB collection using a user query. It   
# converts the query into an embedding using Ollama, retrieves similar records from ChromaDB, and then uses a language model to summarize the retrieved context.
import ollama
import chromadb

# Load existing persistent DB
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("user_inputs")

# User query
user_query = "How can agents use tools?"

# Convert query to embedding
response = ollama.embed(
    model="nomic-embed-text:latest",
    input=user_query
)

query_embedding = response["embeddings"][0]

# Search similar records
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

context= results["documents"]

response = ollama.chat(
    model="llama3",
    messages=[
        {
            "role": "system",
            "content": "Summarize the following information clearly."
        },
        {
            "role": "user",
            "content": f"Context:\n{context}"
        }
    ]
)

print("\nSummary:\n", response["message"]["content"])